"""
.. topic:: Stage (views)

    Este é o módulo que realiza a carga da área de stage.

.. topic:: Ações relacionadas ao módulo

    * Tela inicial: index
    * Carregar tabelas de stage: carregaStage


"""

# stage/views.py

from flask import render_template,url_for,flash, redirect,request,Blueprint,abort
from sqlalchemy import func, distinct, and_, or_
from sqlalchemy.sql import label
from project import db, app

import os
import re
from datetime import datetime as dt
import time
from threading import Thread

from project.models import tr_entregas_grupos

import pymysql
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s] - [%(levelname)s] - %(message)s')
LOGGER = logging.getLogger(__name__)

stage = Blueprint("stage",__name__)

max_data = dt.strptime('9999-12-31','%Y-%m-%d').date()
min_data = dt.strptime('1900-01-01','%Y-%m-%d').date()

# função com queries sql que resgara dados do banco do Petrvs

def consultaPetrvs(**entrada):

    if entrada['tabela'] == 'st_unidades': # unidades no Petrvs
        
        sql = "SELECT unidades.id,\
                      CONCAT(u2.sigla, '/', unidades.sigla) AS sigla,\
                      unidades.nome,\
                      CASE WHEN unidades.unidade_pai_id IS NULL THEN 'N.I.' ELSE unidades.unidade_pai_id END AS unidade_pai_id,\
                      cidades.uf,\
                      CASE WHEN unidades.path IS NULL THEN 'N.I.' ELSE unidades.path END AS path,\
                      CASE WHEN unidades.codigo = '' THEN 'N.I.' ELSE unidades.codigo END AS codigo,\
                      unidades.data_inativacao \
                FROM unidades \
                LEFT OUTER JOIN cidades ON cidades.id = unidades.cidade_id \
                LEFT OUTER JOIN unidades u2 ON u2.id = unidades.unidade_pai_id \
                WHERE unidades.deleted_at IS NULL"
    
    elif entrada['tabela'] == 'st_usuarios': # usuários no Petrvs
        
        sql = "SELECT usuarios.id,\
                      usuarios.nome,\
                      usuarios.email,\
                      usuarios.cpf,\
                      usuarios.matricula,\
                      usuarios.data_nascimento,\
                      usuarios.uf,\
                      usuarios.sexo,\
                      usuarios.situacao_funcional,\
                      usuarios.data_modificacao,\
                      CASE WHEN tipos_modalidades_siape.nome IS NULL THEN 'N.I.' ELSE tipos_modalidades_siape.nome END AS modalidade_pgd,\
                      CASE WHEN usuarios.participa_pgd IS NULL THEN 'N.I.' ELSE usuarios.participa_pgd END AS participa_pgd,\
                      CASE WHEN usuarios.nome_jornada IS NULL THEN 'N.I.' ELSE usuarios.nome_jornada END AS nome_jornada,\
                      CASE WHEN usuarios.cod_jornada IS NULL THEN -1 ELSE usuarios.cod_jornada END AS cod_jornada \
               FROM usuarios \
               LEFT OUTER JOIN tipos_modalidades_siape ON tipos_modalidades_siape.id = usuarios.tipo_modalidade_id \
               WHERE usuarios.deleted_at IS NULL"

    elif entrada['tabela'] == 'st_planos_entregas':
        
        sql = "SELECT planos_entregas.id,\
                      planos_entregas.numero,\
                      planos_entregas.data_inicio,\
                      planos_entregas.data_fim,\
                      planos_entregas.data_arquivamento,\
                      planos_entregas.nome,\
                      planos_entregas.status,\
                      CASE WHEN planos_entregas.planejamento_id IS NULL THEN 'N.I.' ELSE planos_entregas.planejamento_id END AS planejamento_id,\
                      CASE WHEN planos_entregas.cadeia_valor_id IS NULL THEN 'N.I.' ELSE planos_entregas.cadeia_valor_id END AS cadeia_valor_id,\
                      planos_entregas.unidade_id,\
                      planos_entregas.plano_entrega_id,\
                      planos_entregas.programa_id,\
                      CASE WHEN planos_entregas.avaliacao_id IS NULL THEN 'N.I.' ELSE planos_entregas.avaliacao_id END AS avaliacao_id,\
                      CASE WHEN planos_entregas.okr_id IS NULL THEN 'N.I.' ELSE planos_entregas.okr_id END AS okr_id\
               FROM planos_entregas \
               WHERE planos_entregas.deleted_at IS NULL"
        
    elif entrada['tabela'] == 'st_entregas':
        
        sql = "SELECT planos_entregas_entregas.id,\
                      planos_entregas_entregas.homologado,\
                      planos_entregas_entregas.progresso_esperado,\
                      planos_entregas_entregas.progresso_realizado,\
                      planos_entregas_entregas.data_inicio,\
                      planos_entregas_entregas.data_fim,\
                      planos_entregas_entregas.descricao,\
                      planos_entregas_entregas.destinatario,\
                      REGEXP_REPLACE(planos_entregas_entregas.meta, '[^a-zA-Z]+', '') AS meta_tipo,\
                      REGEXP_REPLACE(planos_entregas_entregas.meta, '[^0-9]+', '') AS meta_valor,\
                      REGEXP_REPLACE(planos_entregas_entregas.realizado, '[^a-zA-Z]+', '') AS realizado_tipo,\
                      REGEXP_REPLACE(planos_entregas_entregas.realizado, '[^0-9]+', '') AS realizado_valor,\
                      CASE WHEN planos_entregas_entregas.descricao_meta IS NULL THEN 'N.I.' ELSE planos_entregas_entregas.descricao_meta END AS descricao_meta,\
                      CASE WHEN planos_entregas_entregas.descricao_entrega IS NULL THEN 'N.I.' ELSE planos_entregas_entregas.descricao_entrega END AS descricao_entrega,\
                      planos_entregas_entregas.plano_entrega_id,\
                      CONCAT(u2.sigla, '/', unidades.sigla) AS unidade_sigla,\
                      unidades.nome AS unidade_nome, \
                      unidades.id AS unidade_id \
               FROM planos_entregas_entregas \
               LEFT OUTER JOIN unidades ON unidades.id = planos_entregas_entregas.unidade_id \
               LEFT OUTER JOIN unidades u2 ON u2.id = unidades.unidade_pai_id \
               WHERE planos_entregas_entregas.deleted_at IS NULL AND unidades.deleted_at IS NULL"    

    elif entrada['tabela'] == 'st_planos_trabalho':

        sql = "SELECT planos_trabalhos.id,\
                      planos_trabalhos.carga_horaria,\
                      planos_trabalhos.numero,\
                      planos_trabalhos.data_inicio,\
                      planos_trabalhos.data_fim,\
                      planos_trabalhos.forma_contagem_carga_horaria,\
                      planos_trabalhos.status,\
                      planos_trabalhos.programa_id,\
                      planos_trabalhos.usuario_id,\
                      planos_trabalhos.unidade_id,\
                      planos_trabalhos.tipo_modalidade_id, \
                      CONCAT(u2.sigla, '/', u1.sigla) AS unidade_sigla \
               FROM planos_trabalhos \
               LEFT OUTER JOIN unidades u1 ON u1.id = planos_trabalhos.unidade_id \
               LEFT OUTER JOIN unidades u2 ON u2.id = u1.unidade_pai_id \
               WHERE planos_trabalhos.deleted_at IS NULL AND u1.deleted_at IS NULL"
        
    elif entrada['tabela'] == 'st_planos_trabalhos_entregas':

        sql = "SELECT planos_trabalhos_entregas.id,\
                      planos_trabalhos_entregas.plano_trabalho_id,\
                      CASE WHEN planos_trabalhos_entregas.plano_entrega_entrega_id IS NULL THEN 'N.I.' ELSE planos_trabalhos_entregas.plano_entrega_entrega_id END AS plano_entrega_entrega_id \
               FROM planos_trabalhos_entregas \
               WHERE planos_trabalhos_entregas.deleted_at IS NULL"    
        
    elif entrada['tabela'] == 'st_avaliacoes':
        
        sql = "SELECT avaliacoes.id,\
                      avaliacoes.data_avaliacao,\
                      avaliacoes.nota,\
                      CASE WHEN avaliacoes.recurso IS NULL THEN 'N.I.' ELSE avaliacoes.recurso END AS recurso,\
                      avaliacoes.data_recurso,\
                      usuarios.nome AS avaliador_nome,\
                      tipos_avaliacoes.nome AS tipo_avaliacao_nome,\
                      tipos_avaliacoes.tipo AS tipo_avaliacao_tipo,\
                      tipos_avaliacoes_notas.descricao AS tipo_avaliacao_nota_descricao,\
                      CASE WHEN avaliacoes.plano_entrega_id IS NULL THEN 'N.I.' ELSE avaliacoes.plano_entrega_id END AS plano_entrega_id,\
                      CASE WHEN avaliacoes.plano_trabalho_consolidacao_id IS NULL THEN 'N.I.' ELSE avaliacoes.plano_trabalho_consolidacao_id END AS plano_trabalho_consolidacao_id \
                FROM avaliacoes \
                LEFT OUTER JOIN usuarios ON usuarios.id = avaliacoes.avaliador_id \
                LEFT OUTER JOIN tipos_avaliacoes ON tipos_avaliacoes.id = avaliacoes.tipo_avaliacao_id \
                LEFT OUTER JOIN tipos_avaliacoes_notas ON tipos_avaliacoes_notas.id = avaliacoes.tipo_avaliacao_nota_id \
                WHERE avaliacoes.deleted_at IS NULL AND usuarios.deleted_at IS NULL"     

    elif entrada['tabela'] == 'st_lotacoes':

        sql = "SELECT usuarios.id AS usuario_id,\
                      unidades.id AS unidade_id,\
                      usuarios.nome AS usuario_nome,\
                      unidades.sigla AS unidade_sigla,\
                      unidades.nome AS unidade_nome, \
                      cidades.uf AS unidade_uf \
                FROM usuarios \
                LEFT OUTER JOIN unidades_integrantes ON unidades_integrantes.usuario_id = usuarios.id \
                LEFT OUTER JOIN unidades_integrantes_atribuicoes ON unidades_integrantes_atribuicoes.unidade_integrante_id = unidades_integrantes.id \
                LEFT OUTER JOIN unidades ON unidades.id = unidades_integrantes.unidade_id \
                LEFT OUTER JOIN cidades ON cidades.id = unidades.cidade_id \
                WHERE unidades_integrantes_atribuicoes.atribuicao = 'LOTADO' AND \
                      usuarios.deleted_at IS NULL AND \
                      unidades_integrantes.deleted_at IS NULL AND \
                      unidades_integrantes_atribuicoes.deleted_at IS NULL AND \
                      unidades.deleted_at IS NULL AND \
                      usuarios.deleted_at IS NULL "
    
    elif entrada['tabela'] == 'st_trabalhos':

        sql = "SELECT atividades.id,\
                      atividades.descricao as atividade_descricao,\
                      atividades.status as atividade_status,\
                      atividades.data_distribuicao as atividade_data_distribuicao,\
                      atividades.progresso as atividade_progresso,\
                      DATEDIFF(CAST(data_estipulada_entrega AS DATE), CAST(data_distribuicao AS DATE)) as prazo,\
                      DATEDIFF(CAST(data_entrega AS DATE), CAST(data_distribuicao AS DATE)) as tempo_utilizado,\
                      CASE WHEN tipos_atividades.nome IS NULL THEN 'N.I.' ELSE tipos_atividades.nome END AS tipo_atividade_nome, \
                      CASE WHEN planos_trabalhos_consolidacoes.status IS NULL THEN 'N.I.' ELSE planos_trabalhos_consolidacoes.status END AS plano_trabalho_consolidacao_status,\
                      CASE WHEN avaliacoes.id IS NULL THEN 'N.I.' ELSE avaliacoes.id END AS avaliacao_id, \
                      CASE WHEN planos_entregas_entregas.id IS NULL THEN 'N.I.' ELSE planos_entregas_entregas.id END AS entrega_id, \
                      atividades.usuario_id,\
                      atividades.unidade_id,\
                      atividades.plano_trabalho_consolidacao_id,\
                      CASE WHEN atividades.plano_trabalho_id IS NULL THEN 'N.I.' ELSE atividades.plano_trabalho_id END AS plano_trabalho_id,\
                      planos_trabalhos_entregas.forca_trabalho \
                FROM atividades \
                LEFT OUTER JOIN tipos_atividades ON tipos_atividades.id = atividades.tipo_atividade_id \
                LEFT OUTER JOIN planos_trabalhos_consolidacoes ON planos_trabalhos_consolidacoes.id = atividades.plano_trabalho_consolidacao_id \
                LEFT OUTER JOIN avaliacoes ON avaliacoes.id = planos_trabalhos_consolidacoes.avaliacao_id \
                LEFT OUTER JOIN planos_trabalhos_entregas ON planos_trabalhos_entregas.id = atividades.plano_trabalho_entrega_id \
                LEFT OUTER JOIN planos_entregas_entregas ON planos_entregas_entregas.id = planos_trabalhos_entregas.plano_entrega_entrega_id \
                LEFT OUTER JOIN usuarios ON usuarios.id = atividades.usuario_id \
                LEFT OUTER JOIN unidades ON unidades.id = atividades.unidade_id \
                WHERE atividades.deleted_at IS NULL AND \
                      planos_trabalhos_consolidacoes.deleted_at IS NULL"
    
    else:
        flash('TIPO INVÁLIDO','erro')
        return

    # Conexão com o banco de dados do Petrvs e gravação dos dados na tabela de stage

    try:
        bd_server   = os.environ.get('PETRVS_DB_SERVER')
        bd_database = os.environ.get('PETRVS_DB_DATABASE')
        bd_user     = os.environ.get('PETRVS_DB_USER')
        bd_pwd      = os.environ.get('PETRVS_DB_PWD')
        bd_port     = os.environ.get('PETRVS_DB_PORT')
        connection  = "mysql+pymysql://"+ bd_user +":"+ bd_pwd +"@"+ bd_server +":"+bd_port +"/"+ bd_database

        df = pd.read_sql_query(sql, connection)

    except pymysql.Error as e:
        LOGGER.error(f"Erro de conexão com MySQL: {e}")

    return df

# função de que executa carga de dados do Petrvs nas tabelas de stage

def carrega_stage():

    ## fazer a carga de st_unidades via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_unidades')

        # Trata os dados, se necessário
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_unidades', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_unidades carregada com sucesso.')

    ## fazer a carga de st_usuarios via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_usuarios')

        # Trata os dados, se necessário
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_usuarios', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_usuarios carregada com sucesso.')

    ## fazer a carga de st_planos_entregas via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_planos_entregas')

        # Trata os dados, se necessário
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_planos_entregas', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_planos_entregas carregada com sucesso.')

    ## fazer a carga de st_planos_trabalho via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_planos_trabalho')

        # Trata os dados, se necessário
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_planos_trabalho', con=db.engine, if_exists='replace', index=False)
    
    LOGGER.info('Tabela st_planos_trabalho carregada com sucesso.')

    ## fazer a carga de st_planos_trabalhos_entregas via pandas

    dados = consultaPetrvs(tabela = 'st_planos_trabalhos_entregas')

        # Trata os dados, se necessário
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_planos_trabalhos_entregas', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_planos_trabalhos_entregas carregada com sucesso.')

    ## fazer a carga de st_entregas via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_entregas')

        # Trata os dados, se necessário

        # Se realizado_tipo for diferente de meta_tipo, usar meta_tipo em realizado_tipo
    def corrige_realizado_tipo(row):    
        if row['realizado_tipo'] != row['meta_tipo']:
            return row['meta_tipo']
        else:
            return row['realizado_tipo']
    dados['realizado_tipo'] = dados.apply(corrige_realizado_tipo, axis=1)

        # Se realizado_nota for maior que meta_valor, usar meta_valor em realizado_valor
    def corrige_realizado_valor(row):
        if row['realizado_valor'] == '':
            return '0' 
        try:
            if int(row['realizado_valor']) > int(row['meta_valor']):
                return row['meta_valor']
            else:
                return row['realizado_valor']    
        except:
            return row['realizado_valor']
    dados['realizado_valor'] = dados.apply(corrige_realizado_valor, axis=1)


    grupos_bd = db.session.query(tr_entregas_grupos).all()

    grupos = {}
    
    for g in grupos_bd:

        grupos[g.nome] = (g.desc, g.palavras_chave.replace(" ","").split(','))
 
    def define_grupo(row): 
        for i in grupos:
            for palavra in grupos[i][1]:
                if palavra in row['descricao'].lower():
                    return [i, grupos[i][0]]
        return ['N.I.','N.I.'] 

    dados[['grupo_nome','grupo_desc']] = dados.apply(define_grupo, axis=1, result_type='expand')

        ## Gera tabela de trabalho com as palavras utilizadas nos nomes das entregas

    palavras_ignoradas = ['a ','à ','e ','i ','l ','o ','ao ','ou ', 'da ','das ','de ','do ','dos ','na ','no ','para ','por ','sob ','sobre ','etc ','assim ',
                          'com ','outro ', 'outros ','conforme ', 'em ','via']
    
        # Criando um padrão regex para casar com as palavras ignoradas
        # '\\b' garante o casamento com a palavra inteira e '|' atua como um operador OR para multiplas palavras
    padrao1 = r'[-!@#$%^&*().,;"+?{}]'
    padrao2 = r'\d'
    padrao3 = r'\b(?:' + '|'.join(palavras_ignoradas) + r')\b'
    padrao4 = r'\s{2,}'

    df_1 = pd.DataFrame(columns=['descricao_desmembrada'])

        # Em um novo dataframe, coloca tudo em minúsculas e troca as palavras ignoradas por uma string vazia
    df_1['descricao_desmembrada'] = dados['descricao'].str.lower()\
                                                      .str.replace(padrao1, '', regex=True)\
                                                      .str.replace(padrao2, '', regex=True)\
                                                      .str.replace(padrao3, '', regex=True)\
                                                      .str.replace(padrao4, ' ', regex=True)\
                                                      .str.split(" ")

        # Cria o dataframe que irá armazenar as palavras desmembradas 
    tr_df = pd.DataFrame(columns=['palavra']) 

    for value in df_1['descricao_desmembrada']:
        for item in value:
            tr_df.loc[len(tr_df)] = [item]

        # Remove palavras vazias
    tr_df = tr_df[tr_df['palavra'] != ''] 
        # cria coluna de ids
    tr_df['id'] = tr_df.index       
        # Joga tr_df em uma tabela de trabalho
    tr_df.to_sql(name='tr_entregas_palavras', con=db.engine, if_exists='replace', index=False)

        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_entregas', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_entregas carregada com sucesso.')

    ## fazer a carga de st_avaliacoes via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_avaliacoes')

        # Trata os dados, se necessário
    dados['nota'] = dados['nota'].str.strip('"\\')
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_avaliacoes', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_avaliacoes carregada com sucesso.')

    ## fazer a carga de st_lotacoes via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_lotacoes')

        # Trata os dados, se necessário
    dados['id'] = range(1, len(dados) + 1)
    
        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_lotacoes', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_lotacoes carregada com sucesso.')

    ## fazer a carga de st_trabalhos via pandas

        # Traz o dataframe com os dados obtidos do sql no banco do Petrvs
    dados = consultaPetrvs(tabela = 'st_trabalhos')

        # Trata os dados, se necessário

        ## Identifica descrições que não são textos relevantes
    def identifica_nao_texto(row):
        pattern = r'^[^a-zA-Z0-9]+|^$$'
        if bool(re.fullmatch(pattern, row['atividade_descricao'])):
            return ['N.I.']
        else:
            return [row['atividade_descricao']]
        
    dados[['atividade_descricao']] = dados.apply(identifica_nao_texto, axis=1, result_type='expand')    

        # Joga os dados do dataframe na tabela de stage
    dados.to_sql(name='st_trabalhos', con=db.engine, if_exists='replace', index=False)

    LOGGER.info('Tabela st_trabalhos carregada com sucesso.')

    return


@stage.route('/carregaStage')
def carregaStage():
    """
    +---------------------------------------------------------------------------------------+
    |Faz a carga da área de Stage.                                                          |
    +---------------------------------------------------------------------------------------+
    """

    start_time = time.perf_counter()

    carrega_stage()

    end_time = time.perf_counter()
    
    elapsed_time = (end_time - start_time)/60
    LOGGER.info(f'Tempo total de carga das tabelas de stage: {elapsed_time:.2f} minutos.')

    flash('Tabelas de stage carregadas com sucesso!','sucesso')

    return render_template ('index.html')







