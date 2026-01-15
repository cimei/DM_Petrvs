"""
.. topic:: dim_fat (views)

    Este é o módulo das dimensões e fatos do DM.

.. topic:: Ações relacionadas ao módulo

    * Tela inicial: index
    * Carregar tabelas de stage: carregaStage


"""

# dim_fat/views.py

from flask import render_template, url_for, flash, redirect,request,Blueprint,abort
from sqlalchemy import func, distinct, and_, or_, cast, Date
from sqlalchemy.sql import label
from sqlalchemy.orm import aliased
from project import db, app
from project.models import st_unidades, st_usuarios, st_planos_entregas, st_planos_trabalho,\
                           st_planos_trabalhos_entregas, st_entregas, st_avaliacoes, st_trabalhos,\
                           di_tempo, di_unidades, di_usuarios, di_planos_entregas, di_planos_trabalho,\
                           di_avaliacoes, di_trabalhos, di_entregas, ft_entregas, tr_ft_entregas, ft_desempenho

from project.dim_fat.forms import FatoForm
import os
import datetime
from datetime import datetime as dt, date, timedelta
import time

import pymysql
import pandas as pd
import logging
from threading import Thread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
LOGGER = logging.getLogger(__name__)

dim_fat = Blueprint("dim_fat",__name__)


################################
# Função para popular a di_tempo
###############################

def populando_di_tempo(data_ini: date, data_fim: date):
    """
    Preenche a tabela di_tempo com as datas de um intervalo específico.
    """

    # Limpa tabela di_tempo
    db.session.query(di_tempo).delete()
    db.session.commit()
    LOGGER.info(f'...')
    LOGGER.info(f'Dimensão di_tempo esvaziada.')

    # Loop para preencher a tabela di_tempo
    data_inserir = data_ini
    while data_inserir <= data_fim:
        
        # Principais dados do dia
        ano             = data_inserir.year
        mes             = data_inserir.month
        dia             = data_inserir.day
        quinzena        = (data_inserir.month - 1) // 3 + 1
        semana          = data_inserir.isocalendar()[1]
        dia_semana      = data_inserir.strftime('%A')
        mes_nome        = data_inserir.strftime('%B')

        # Determina se o dia esta num final de semana
        final_de_semana = data_inserir.weekday() >= 5  # Sábado (5) or Domingo (6)

        # Determina o bimestre

        if mes in [1, 2]:
            bimestre = 1
        elif mes in [3, 4]:
            bimestre = 2
        elif mes in [5, 6]:
            bimestre = 3
        elif mes in [7, 8]:
            bimestre = 4
        elif mes in [9, 10]:
            bimestre = 5
        else:
            bimestre = 6
        
        nome_bimestre = f'{bimestre}º Bimestre/{ano}'

        # Determina o trimestre

        if mes in [1, 2, 3]:
            trimestre = 1
        elif mes in [4, 5, 6]:
            trimestre = 2
        elif mes in [7, 8, 9]:
            trimestre = 3
        else:
            trimestre = 4

        nome_trimestre = f'{trimestre}º Trimestre/{ano}'

        # Determina o quadrimestre
        if mes in [1, 2, 3, 4]:
            quadrimestre = 1
        elif mes in [5, 6, 7, 8]:
            quadrimestre = 2
        else:
            quadrimestre = 3

        nome_quadrimestre = f'{quadrimestre}º Quadrimestre/{ano}'

        # Determina o semestre

        if mes in [1, 2, 3, 4, 5, 6]:
            semestre = 1
        else:
            semestre = 2

        nome_semestre = f'{semestre}º Semestre/{ano}'

        # Verifica se é feriado - falta implementar

        feriado = False

        # Cria o objeto di_tempo
        registra_tempo = di_tempo(db_data           = data_inserir,
                                    ano               = ano,
                                    mes               = mes,
                                    dia               = dia,
                                    quinzena          = quinzena,
                                    semana            = semana,
                                    dia_semana        = dia_semana,
                                    mes_nome          = mes_nome,
                                    final_de_semana   = final_de_semana,
                                    feriado           = feriado,
                                    bimestre          = bimestre,
                                    nome_bimestre     = nome_bimestre,  
                                    trimestre         = trimestre,
                                    nome_trimestre    = nome_trimestre,
                                    quadrimestre      = quadrimestre,
                                    nome_quadrimestre = nome_quadrimestre,
                                    semestre          = semestre,
                                    nome_semestre     = nome_semestre)  
        
        db.session.add(registra_tempo)
        data_inserir += timedelta(days=1)
    
    db.session.commit()
    LOGGER.info(f'Dimensão di_tempo preenchida.')


################################
# função que executa cargas das dimensões
###############################

def carga_dimensoes():
    """ 
    Preenche as tabelas de dimensão.
    """
    
    # Criando a di_unidades

        # Limpa tabela di_unidades
    db.session.query(di_unidades).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_unidades esvaziada.')

        # Lê os dados da st_unidades     
    ler_st_unidades = st_unidades.query.all()

        # Popula a di_unidades  
    for unidade in ler_st_unidades:

        if unidade.data_inativacao == None:
            data_inativacao = None
        else:
            # data_inativacao = dt.strptime(unidade.data_inativacao,'%Y-%m-%d 00:00:00.000')
            data_inativacao = unidade.data_inativacao

        nova_unidade = di_unidades(id              = unidade.id,
                                   sigla           = unidade.sigla,
                                   nome            = unidade.nome,
                                   unidade_pai_id  = unidade.unidade_pai_id,
                                   uf              = unidade.uf,
                                   path            = unidade.path,
                                   codigo          = unidade.codigo,
                                   data_inativacao = data_inativacao)
        
        db.session.add(nova_unidade)

    db.session.commit()
    LOGGER.info(f'Dimensão di_unidades preenchida.')

    # Criando a di_usuarios

        # Limpa tabela di_usuarios
    db.session.query(di_usuarios).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_usuarios esvaziada.')

        # Lê os dados da st_usuarios
    ler_st_usuarios = st_usuarios.query.all()
    
        # Popula a di_usuarios
    for usuario in ler_st_usuarios:
        novo_usuario = di_usuarios(id                       = usuario.id,
                                   nome                     = usuario.nome,
                                   email                    = usuario.email,
                                   cpf                      = usuario.cpf,
                                   matricula                = usuario.matricula,
                                   data_nascimento          = usuario.data_nascimento,
                                   uf                       = usuario.uf,
                                   sexo                     = usuario.sexo,
                                   situacao_funcional       = usuario.situacao_funcional,
                                   data_modificacao         = usuario.data_modificacao,
                                   modalidade_pgd           = usuario.modalidade_pgd,
                                   participa_pgd            = usuario.participa_pgd,
                                   nome_jornada             = usuario.nome_jornada,
                                   cod_jornada              = usuario.cod_jornada)
        
        db.session.add(novo_usuario)
    db.session.commit()    
    LOGGER.info(f'Dimensão di_usuarios preenchida.')

    # Criando a di_planos_entregas

        # Limpa tabela di_planos_entregas
    db.session.query(di_planos_entregas).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_planos_entregas esvaziada.')

        # Lê os dados da st_planos_entregas
    ler_st_planos_entregas = st_planos_entregas.query.all()

        # Popula a di_planos_entregas
    for plano_entrega in ler_st_planos_entregas:
        novo_plano_entrega = di_planos_entregas(id                = plano_entrega.id,
                                                numero            = plano_entrega.numero,
                                                data_inicio       = plano_entrega.data_inicio,
                                                data_fim          = plano_entrega.data_fim,
                                                data_arquivamento = plano_entrega.data_arquivamento,
                                                nome              = plano_entrega.nome,
                                                status            = plano_entrega.status)
        
        db.session.add(novo_plano_entrega)
    db.session.commit()
    LOGGER.info(f'Dimensão di_planos_entregas preenchida.')

    # Criando a di_planos_trabalho

        # Limpa tabela di_planos_trabalho
    db.session.query(di_planos_trabalho).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_planos_trabalho esvaziada.')

        # Lê os dados da st_planos_trabalho
    ler_st_planos_trabalho = st_planos_trabalho.query.all()

        # Popula a di_planos_trabalho
    for plano_trabalho in ler_st_planos_trabalho:
        novo_plano_trabalho = di_planos_trabalho(id                           = plano_trabalho.id,
                                                 carga_horaria                = plano_trabalho.carga_horaria,
                                                 numero                       = plano_trabalho.numero,
                                                 data_inicio                  = plano_trabalho.data_inicio,
                                                 data_fim                     = plano_trabalho.data_fim,
                                                 forma_contagem_carga_horaria = plano_trabalho.forma_contagem_carga_horaria,
                                                 status                       = plano_trabalho.status)
        
        db.session.add(novo_plano_trabalho)
    db.session.commit()
    LOGGER.info(f'Dimensão di_planos_trabalho preenchida.')

    # Criando di_avaliacoes

        # Limpa tabela di_avaliacoes
    db.session.query(di_avaliacoes).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_avaliacoes esvaziada.')

        # Lê os dados da st_avaliacoes
    ler_st_avaliacoes = st_avaliacoes.query.all()

        # Popula a di_avaliacoes
    for avaliacao in ler_st_avaliacoes:

        if avaliacao.data_recurso == None:
            data_recurso = None
        else:
            # data_recurso = dt.strptime(avaliacao.data_recurso,'%Y-%m-%d 00:00:00.000')  
            data_recurso = avaliacao.data_recurso  

        nova_avaliacao = di_avaliacoes(id                   = avaliacao.id,
                                        data_avaliacao      = avaliacao.data_avaliacao,
                                        nota                = avaliacao.nota,
                                        recurso             = avaliacao.recurso,
                                        data_recurso        = data_recurso,
                                        avaliador_nome      = avaliacao.avaliador_nome,
                                        tipo_avaliacao_nome = avaliacao.tipo_avaliacao_nome,
                                        tipo_avaliacao_tipo = avaliacao.tipo_avaliacao_tipo,
                                        tipo_avaliacao_nota_descricao  = avaliacao.tipo_avaliacao_nota_descricao,
                                        plano_entrega_id               = avaliacao.plano_entrega_id,
                                        plano_trabalho_consolidacao_id = avaliacao.plano_trabalho_consolidacao_id) 
        
        db.session.add(nova_avaliacao)
    db.session.commit()
    LOGGER.info(f'Dimensão di_avaliacoes preenchida.')

        # Criando di_trabalhos

        # Limpa tabela di_trabalhos
    db.session.query(di_trabalhos).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_trabalhos esvaziada.')

        # Lê os dados da st_trabalhos
    ler_st_trabalhos = st_trabalhos.query.all()

        # Popula a di_trabalhos
    for trabalho in ler_st_trabalhos: 

        novo_trabalho = di_trabalhos(id                                  = trabalho.id,
                                     atividade_data_distribuicao         = trabalho.atividade_data_distribuicao,
                                     atividade_descricao                 = trabalho.atividade_descricao,
                                     atividade_status                    = trabalho.atividade_status,
                                     atividade_progresso                 = trabalho.atividade_progresso,
                                     prazo                               = trabalho.prazo,
                                     tempo_utilizado                     = trabalho.tempo_utilizado,
                                     tipo_atividade_nome                 = trabalho.tipo_atividade_nome,
                                     plano_trabalho_consolidacao_status  = trabalho.plano_trabalho_consolidacao_status,
                                     avaliacao_id                        = trabalho.avaliacao_id,
                                     entrega_id                          = trabalho.entrega_id,
                                     usuario_id                          = trabalho.usuario_id,
                                     unidade_id                          = trabalho.unidade_id,
                                     plano_trabalho_id                   = trabalho.plano_trabalho_id,
                                     forca_trabalho                      = trabalho.forca_trabalho) 
        
        db.session.add(novo_trabalho)
    db.session.commit()
    LOGGER.info(f'Dimensão di_trabalhos preenchida.')

        # Criando di_entregas

        # Limpa tabela di_entregas
    db.session.query(di_entregas).delete()
    db.session.commit()
    LOGGER.info(f'Dimensão di_entregas esvaziada.')

        # Lê os dados da st_entregas
    ler_st_entregas = st_entregas.query.all()

        # Popula a di_entregas
    for entrega in ler_st_entregas: 

        nova_entrega = di_entregas(id                  = entrega.id,
                                   homologado          = entrega.homologado,
                                   progresso_esperado  = entrega.progresso_esperado,
                                   progresso_realizado = entrega.progresso_realizado,
                                   data_inicio         = entrega.data_inicio,
                                   data_fim            = entrega.data_fim,
                                   descricao           = entrega.descricao,
                                   destinatario        = entrega.destinatario,
                                   meta_tipo           = entrega.meta_tipo,
                                   meta_valor          = entrega.meta_valor,
                                   realizado_tipo      = entrega.realizado_tipo,
                                   realizado_valor     = entrega.realizado_valor,
                                   descricao_meta      = entrega.descricao_meta,
                                   descricao_entrega   = entrega.descricao_entrega,
                                   plano_entrega_id    = entrega.plano_entrega_id,
                                   unidade_sigla       = entrega.unidade_sigla,
                                   unidade_nome        = entrega.unidade_nome,
                                   unidade_id          = entrega.unidade_id,
                                   grupo_nome          = entrega.grupo_nome,
                                   grupo_desc          = entrega.grupo_desc)
        
        db.session.add(nova_entrega)
    db.session.commit()
    LOGGER.info(f'Dimensão di_entregas preenchida.')


################################
# Função para criar a ft_entregas
###############################

# def carga_ft_entregas(*args):
#     """ 
#     Preenche a tabela fato ft_entregas.
#     """
#     with app.app_context():
        
#         start_time = time.perf_counter()

        
#         if 'di_tempo' in args:

#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()
#             LOGGER.info(f'...')
#             LOGGER.info(f'Fato ft_entregas esvaziada.')

#             LOGGER.info(f'Iniciando construção de ft_entregas, já conectanto com di_tempo.')

#             tempo_1 = aliased(di_tempo)
#             tempo_2 = aliased(di_tempo)
#             # Junta st_entregas com di_tempo (pegando sk da dimensão)
#             ft_entregas_tempo = db.session.query(st_entregas.id,
#                                                  st_entregas.data_inicio,
#                                                  st_entregas.data_fim,
#                                                  st_entregas.descricao,
#                                                  st_entregas.destinatario,
#                                                  st_entregas.meta,
#                                                  st_entregas.unidade_sigla,
#                                                  st_entregas.unidade_nome,
#                                                  st_entregas.grupo_nome, 
#                                                  st_entregas.grupo_desc,
#                                                  label('tempo_ini_id', tempo_1.id),
#                                                  label('tempo_fim_id', tempo_2.id)) \
#                                     .join(tempo_1, cast(st_entregas.data_inicio, Date) == cast(tempo_1.db_data, Date)) \
#                                     .join(tempo_2, cast(st_entregas.data_fim, Date) == cast (tempo_2.db_data, Date)) \
#                                     .all()
            
#             LOGGER.info(f'  ft_entregas com di_tempo: {len(ft_entregas_tempo)} registros.')
#             for item in ft_entregas_tempo:  # percorre os resultados do join e cria regisrtros na ft_entregas, um a um.
#                 ## Aqui ft_entregas é criada, pois recebe dados pela primeira vez
#                 nova_ft_entrega = ft_entregas(di_unidades_id        = -1,
#                                               di_usuarios_id        = -1,
#                                               di_planos_entregas_id = -1,
#                                               di_planos_trabalho_id = -1,
#                                               di_avaliacao_id       = -1,
#                                               di_trabalhos_id       = -1,
#                                               di_tempo_ini_id       = item.tempo_ini_id,
#                                               di_tempo_fim_id       = item.tempo_fim_id,
#                                               data_inicio           = item.data_inicio,
#                                               data_fim              = item.data_fim,
#                                               descricao             = item.descricao,
#                                               destinatario          = item.destinatario,
#                                               meta                  = item.meta,
#                                               entrega_id            = item.id,
#                                               unidade_sigla         = item.unidade_sigla,
#                                               unidade_nome          = item.unidade_nome,
#                                               grupo_nome            = item.grupo_nome,
#                                               grupo_desc            = item.grupo_desc)
                
#                 db.session.add(nova_ft_entrega)  
#             db.session.commit()
#             LOGGER.info(f'  ft_entregas criada e conectada com di_tempo.')

#         if 'di_planos_entregas' in args:
#             LOGGER.info(f'Iniciando ligação da ft_entregas com di_planos_entregas.')   
#             # Join da ft_entregas com di_planos_entregas, pegando sk da dimensão
#             ft_entregas_pe = db.session.query(ft_entregas.entrega_id,
#                                               ft_entregas.di_tempo_ini_id,
#                                               ft_entregas.di_tempo_fim_id,
#                                               di_planos_entregas.di_planos_entregas_id,
#                                               ft_entregas.data_inicio,
#                                               ft_entregas.data_fim,
#                                               ft_entregas.descricao,
#                                               ft_entregas.destinatario,
#                                               ft_entregas.meta,
#                                               ft_entregas.unidade_sigla,
#                                               ft_entregas.unidade_nome,
#                                               ft_entregas.grupo_nome, 
#                                               ft_entregas.grupo_desc)\
#                                     .join(st_entregas, ft_entregas.entrega_id == st_entregas.id)\
#                                     .outerjoin(di_planos_entregas, st_entregas.plano_entrega_id == di_planos_entregas.id)\
#                                     .all()
#             LOGGER.info(f'  ft_entregas com di_planos_entregas: {len(ft_entregas_pe)} registros. Não admitindo entregas órfãs')
#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()

#             for item in ft_entregas_pe:
#                 if item.di_planos_entregas_id != None:  # Só insere se houver plano de entrega (não admitindo entregas órfãs)
#                     nova_ft_entrega = ft_entregas(di_unidades_id        = -1,
#                                                   di_usuarios_id        = -1,
#                                                   di_planos_trabalho_id = -1,
#                                                   di_avaliacao_id       = -1,
#                                                   di_trabalhos_id       = -1,
#                                                   di_planos_entregas_id = item.di_planos_entregas_id,
#                                                   di_tempo_ini_id       = item.di_tempo_ini_id,
#                                                   di_tempo_fim_id       = item.di_tempo_fim_id,
#                                                   data_inicio           = item.data_inicio,
#                                                   data_fim              = item.data_fim,
#                                                   descricao             = item.descricao,
#                                                   destinatario          = item.destinatario,
#                                                   meta                  = item.meta,
#                                                   entrega_id            = item.entrega_id,
#                                                   unidade_sigla         = item.unidade_sigla,
#                                                   unidade_nome          = item.unidade_nome,
#                                                   grupo_nome            = item.grupo_nome,
#                                                   grupo_desc            = item.grupo_desc)
            
#                     db.session.add(nova_ft_entrega)
#             db.session.commit()
#             LOGGER.info(f'  ft_entregas conectada com di_planos_entregas.')


#         if 'di_unidades_e_di_usuarios' in args:
#             LOGGER.info(f'Iniciando ligação da ft_entregas com di_unidades e di_usuarios.')
#             # Juntando entregas com usuarios e unidades (pegando chaves substitutas)
#             entregas_usu_unid = db.session.query(ft_entregas.entrega_id,
#                                                  di_usuarios.di_usuarios_id,
#                                                  di_unidades.di_unidades_id,
#                                                  ft_entregas.di_tempo_ini_id,
#                                                  ft_entregas.di_tempo_fim_id,
#                                                  ft_entregas.di_planos_entregas_id,
#                                                  ft_entregas.data_inicio,
#                                                  ft_entregas.data_fim,
#                                                  ft_entregas.descricao,
#                                                  ft_entregas.destinatario,
#                                                  ft_entregas.meta,
#                                                  ft_entregas.unidade_sigla,
#                                                  ft_entregas.unidade_nome,
#                                                  ft_entregas.grupo_nome, 
#                                                  ft_entregas.grupo_desc)\
#                                 .outerjoin(st_planos_trabalhos_entregas, ft_entregas.entrega_id == st_planos_trabalhos_entregas.plano_entrega_entrega_id)\
#                                 .outerjoin(st_planos_trabalho, st_planos_trabalhos_entregas.plano_trabalho_id == st_planos_trabalho.id)\
#                                 .outerjoin(di_usuarios, st_planos_trabalho.usuario_id == di_usuarios.id)\
#                                 .outerjoin(di_unidades, st_planos_trabalho.unidade_id == di_unidades.id)\
#                                 .all()
#             LOGGER.info(f'  ft_entregas com di_unidades e di_usuarios: {len(entregas_usu_unid)} registros.')
#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()

#             for item in entregas_usu_unid:  
#                 if item.di_unidades_id is None:
#                     un_sk = -1
#                 else:   
#                     un_sk = item.di_unidades_id

#                 if item.di_usuarios_id is None:
#                     us_sk = -1
#                 else:   
#                     us_sk = item.di_usuarios_id 

#                 nova_ft_entrega = ft_entregas(di_planos_trabalho_id = -1,
#                                               di_avaliacao_id       = -1,
#                                               di_trabalhos_id       = -1,
#                                               di_unidades_id        = un_sk,
#                                               di_usuarios_id        = us_sk,
#                                               di_planos_entregas_id = item.di_planos_entregas_id,
#                                               di_tempo_ini_id       = item.di_tempo_ini_id,
#                                               di_tempo_fim_id       = item.di_tempo_fim_id,
#                                               data_inicio           = item.data_inicio,
#                                               data_fim              = item.data_fim,
#                                               descricao             = item.descricao,
#                                               destinatario          = item.destinatario,
#                                               meta                  = item.meta,
#                                               entrega_id            = item.entrega_id,
#                                               unidade_sigla         = item.unidade_sigla,
#                                               unidade_nome          = item.unidade_nome,
#                                               grupo_nome            = item.grupo_nome,
#                                               grupo_desc            = item.grupo_desc)
            
#                 db.session.add(nova_ft_entrega)  
#             db.session.commit()
#             LOGGER.info(f'  ft_entregas conectada com com di_unidades e di_usuarios.')

#         if 'di_planos_trabalho' in args:
#             LOGGER.info(f'Iniciando ligação da ft_entregas com di_planos_trabalho.')
#             # Limpa tabela tr_ft_entregas
#             db.session.query(tr_ft_entregas).delete()
#             db.session.commit()
#             # Criar ft_entregas provisória (tr_ft_entregas)
#             le_ft_entregas = db.session.query(ft_entregas).all()
#             for entrega in le_ft_entregas:
#                 nova_tr_ft_entregas = tr_ft_entregas( ft_entregas_id        = entrega.ft_entregas_id,
#                                                       di_unidades_id        = entrega.di_unidades_id,
#                                                       di_usuarios_id        = entrega.di_usuarios_id,
#                                                       di_planos_entregas_id = entrega.di_planos_entregas_id,
#                                                       di_planos_trabalho_id = entrega.di_planos_trabalho_id,
#                                                       di_avaliacao_id       = entrega.di_avaliacao_id,
#                                                       di_trabalhos_id       = entrega.di_trabalhos_id,
#                                                       di_tempo_ini_id       = entrega.di_tempo_ini_id,
#                                                       di_tempo_fim_id       = entrega.di_tempo_fim_id,
#                                                       data_inicio           = entrega.data_inicio,
#                                                       data_fim              = entrega.data_fim,
#                                                       descricao             = entrega.descricao,
#                                                       destinatario          = entrega.destinatario,
#                                                       meta                  = entrega.meta,
#                                                       entrega_id            = entrega.entrega_id,
#                                                       unidade_sigla         = entrega.unidade_sigla,
#                                                       unidade_nome          = entrega.unidade_nome,
#                                                       grupo_nome            = entrega.grupo_nome,
#                                                       grupo_desc            = entrega.grupo_desc)
#                 db.session.add(nova_tr_ft_entregas)
#             db.session.commit() 

#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()   

#             ultimo_id = 0
#             tamanho_lote = 200000
#             lote = 0
#             registros = 0

#             while True:
#                 lote += 1
#                 LOGGER.info(f'  Processando lote {lote} na junção ft_entregas e di_planos_trabalho...')
#                 # Juntando entregas com planos de trabalho (pegando chaves substitutas)
#                 ft_entregas_pt = db.session.query(tr_ft_entregas.ft_entregas_id,
#                                                 tr_ft_entregas.entrega_id,
#                                                 di_planos_trabalho.di_planos_trabalho_id,
#                                                 tr_ft_entregas.di_usuarios_id,
#                                                 tr_ft_entregas.di_unidades_id,
#                                                 tr_ft_entregas.di_planos_entregas_id,
#                                                 tr_ft_entregas.di_tempo_ini_id,
#                                                 tr_ft_entregas.di_tempo_fim_id,
#                                                 tr_ft_entregas.data_inicio,
#                                                 tr_ft_entregas.data_fim,
#                                                 tr_ft_entregas.descricao,
#                                                 tr_ft_entregas.destinatario,
#                                                 tr_ft_entregas.meta,
#                                                 tr_ft_entregas.unidade_sigla,
#                                                 tr_ft_entregas.unidade_nome,
#                                                 tr_ft_entregas.grupo_nome, 
#                                                 tr_ft_entregas.grupo_desc)\
#                                         .outerjoin(st_planos_trabalhos_entregas, tr_ft_entregas.entrega_id == st_planos_trabalhos_entregas.plano_entrega_entrega_id)\
#                                         .outerjoin(di_planos_trabalho, st_planos_trabalhos_entregas.plano_trabalho_id == di_planos_trabalho.id)\
#                                         .filter(tr_ft_entregas.ft_entregas_id > ultimo_id) \
#                                         .order_by(tr_ft_entregas.ft_entregas_id)\
#                                         .limit(tamanho_lote)\
#                                         .all()
#                 if not ft_entregas_pt:
#                     break
                
#                 for item in ft_entregas_pt:

#                     registros += 1

#                     if item.di_planos_trabalho_id is None:
#                         pt_sk = -1
#                     else:   
#                         pt_sk = item.di_planos_trabalho_id
                    
#                     nova_ft_entrega = ft_entregas( di_avaliacao_id       = -1,
#                                                    di_trabalhos_id       = -1,
#                                                    di_planos_trabalho_id = pt_sk,
#                                                    di_unidades_id        = item.di_unidades_id,
#                                                    di_usuarios_id        = item.di_usuarios_id,
#                                                    di_planos_entregas_id = item.di_planos_entregas_id,
#                                                    di_tempo_ini_id       = item.di_tempo_ini_id,
#                                                    di_tempo_fim_id       = item.di_tempo_fim_id,
#                                                    data_inicio           = item.data_inicio,
#                                                    data_fim              = item.data_fim,
#                                                    descricao             = item.descricao,
#                                                    destinatario          = item.destinatario,
#                                                    meta                  = item.meta,
#                                                    entrega_id            = item.entrega_id,
#                                                    unidade_sigla         = item.unidade_sigla,
#                                                    unidade_nome          = item.unidade_nome,
#                                                    grupo_nome            = item.grupo_nome,
#                                                    grupo_desc            = item.grupo_desc)
                
#                     db.session.add(nova_ft_entrega)
#                 db.session.commit()

#                 ultimo_id = ft_entregas_pt[-1].ft_entregas_id

#             LOGGER.info(f'  ft_entregas com di_planos_trabalho: Cerca de {registros} registros.')
#             LOGGER.info(f'ft_entregas conectada com di_planos_trabalho.')

#         if 'di_avaliacoes' in args:
#             # Juntando entregas com avaliações (pegando chaves substitutas)
#             LOGGER.info(f'Iniciando ligação da ft_entregas com di_avaliacoes.')
#             # Limpa tabela tr_ft_entregas
#             db.session.query(tr_ft_entregas).delete()
#             db.session.commit()

#             # Carrega ft_entregas provisória (tr_ft_entregas)
#             ultimo_id = 0
#             tamanho_lote = 100000
#             lote = 0
#             registros = 0

#             while True:
#                 lote += 1
#                 LOGGER.info(f'  Lendo ft_entregas em lotes: Lote {lote} ...')
#                 le_ft_entregas = db.session.query(ft_entregas)\
#                                            .filter(ft_entregas.ft_entregas_id > ultimo_id) \
#                                            .order_by(ft_entregas.ft_entregas_id)\
#                                            .limit(tamanho_lote)\
#                                            .all()
#                 if not le_ft_entregas:
#                     break
            
#                 for entrega in le_ft_entregas:

#                     nova_tr_ft_entregas = tr_ft_entregas( ft_entregas_id        = entrega.ft_entregas_id,
#                                                         di_unidades_id        = entrega.di_unidades_id,
#                                                         di_usuarios_id        = entrega.di_usuarios_id,
#                                                         di_planos_entregas_id = entrega.di_planos_entregas_id,
#                                                         di_planos_trabalho_id = entrega.di_planos_trabalho_id,
#                                                         di_avaliacao_id       = entrega.di_avaliacao_id,
#                                                         di_trabalhos_id       = entrega.di_trabalhos_id,
#                                                         di_tempo_ini_id       = entrega.di_tempo_ini_id,
#                                                         di_tempo_fim_id       = entrega.di_tempo_fim_id,
#                                                         data_inicio           = entrega.data_inicio,
#                                                         data_fim              = entrega.data_fim,
#                                                         descricao             = entrega.descricao,
#                                                         destinatario          = entrega.destinatario,
#                                                         meta                  = entrega.meta,
#                                                         entrega_id            = entrega.entrega_id,
#                                                         unidade_sigla         = entrega.unidade_sigla,
#                                                         unidade_nome          = entrega.unidade_nome,
#                                                         grupo_nome            = entrega.grupo_nome,
#                                                         grupo_desc            = entrega.grupo_desc)
#                     db.session.add(nova_tr_ft_entregas)
#                 db.session.commit()
#                 ultimo_id = le_ft_entregas[-1].ft_entregas_id 

#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()   

#             ultimo_id = 0
#             tamanho_lote = 200000
#             lote = 0

#             while True:
#                 lote += 1
#                 LOGGER.info(f'  Processando lote {lote} na junção ft_entregas e di_avaliacoes...')
#                 ft_entregas_aval = db.session.query(tr_ft_entregas.ft_entregas_id,
#                                                     tr_ft_entregas.entrega_id,
#                                                     di_avaliacoes.di_avaliacao_id,
#                                                     tr_ft_entregas.di_usuarios_id,
#                                                     tr_ft_entregas.di_unidades_id,
#                                                     tr_ft_entregas.di_planos_entregas_id,
#                                                     tr_ft_entregas.di_planos_trabalho_id,
#                                                     tr_ft_entregas.di_tempo_ini_id,
#                                                     tr_ft_entregas.di_tempo_fim_id,
#                                                     tr_ft_entregas.data_inicio,
#                                                     tr_ft_entregas.data_fim,
#                                                     tr_ft_entregas.descricao,
#                                                     tr_ft_entregas.destinatario,
#                                                     tr_ft_entregas.meta,
#                                                     tr_ft_entregas.unidade_sigla,
#                                                     tr_ft_entregas.unidade_nome,
#                                                     tr_ft_entregas.grupo_nome, 
#                                                     tr_ft_entregas.grupo_desc)\
#                                             .join(st_entregas, tr_ft_entregas.entrega_id == st_entregas.id)\
#                                             .outerjoin(di_avaliacoes, st_entregas.plano_entrega_id == di_avaliacoes.plano_entrega_id)\
#                                             .filter(tr_ft_entregas.ft_entregas_id > ultimo_id) \
#                                             .order_by(tr_ft_entregas.ft_entregas_id)\
#                                             .limit(tamanho_lote)\
#                                             .all()
            
#                 if not ft_entregas_aval:
#                     break

#                 for item in ft_entregas_aval:

#                     registros += 1

#                     if item.di_avaliacao_id is None:
#                         av_sk = -1
#                     else:   
#                         av_sk = item.di_avaliacao_id
                    
#                     nova_ft_entrega = ft_entregas(di_trabalhos_id       = -1,
#                                                 di_avaliacao_id       = av_sk,
#                                                 di_unidades_id        = item.di_unidades_id,
#                                                 di_usuarios_id        = item.di_usuarios_id,
#                                                 di_planos_entregas_id = item.di_planos_entregas_id,
#                                                 di_planos_trabalho_id = item.di_planos_trabalho_id,
#                                                 di_tempo_ini_id       = item.di_tempo_ini_id,
#                                                 di_tempo_fim_id       = item.di_tempo_fim_id,
#                                                 data_inicio           = item.data_inicio,
#                                                 data_fim              = item.data_fim,
#                                                 descricao             = item.descricao,
#                                                 destinatario          = item.destinatario,
#                                                 meta                  = item.meta,
#                                                 entrega_id            = item.entrega_id,
#                                                 unidade_sigla         = item.unidade_sigla,
#                                                 unidade_nome          = item.unidade_nome,
#                                                 grupo_nome            = item.grupo_nome, 
#                                                 grupo_desc            = item.grupo_desc)
                
#                     db.session.add(nova_ft_entrega)
#                 db.session.commit()

#                 ultimo_id = ft_entregas_aval[-1].ft_entregas_id

#             LOGGER.info(f'  ft_entregas com di_avaliacoes: Cerca de {registros} registros.')
#             LOGGER.info(f'ft_entregas conectada com di_avaliacoes.')

#         if 'di_trabalhos' in args:
#             # Juntando entregas com trabahos (pegando chaves substitutas)
#             LOGGER.info(f'Iniciando ligação da ft_entregas com di_trabalhos.')
#             # Limpa tabela tr_ft_entregas
#             db.session.query(tr_ft_entregas).delete()
#             db.session.commit()

#             # Carrega ft_entregas provisória (tr_ft_entregas)
#             ultimo_id = 0
#             tamanho_lote = 100000
#             lote = 0
#             registros = 0
            
#             while True:
#                 lote += 1
#                 LOGGER.info(f'  Lendo ft_entregas em lotes: Lote {lote} ...')
#                 le_ft_entregas = db.session.query(ft_entregas)\
#                                            .filter(ft_entregas.ft_entregas_id > ultimo_id) \
#                                             .order_by(ft_entregas.ft_entregas_id)\
#                                             .limit(tamanho_lote)\
#                                             .all()
#                 if not le_ft_entregas:
#                     break

#                 for entrega in le_ft_entregas:

#                     nova_tr_ft_entregas = tr_ft_entregas( ft_entregas_id        = entrega.ft_entregas_id,
#                                                         di_unidades_id        = entrega.di_unidades_id,
#                                                         di_usuarios_id        = entrega.di_usuarios_id,
#                                                         di_planos_entregas_id = entrega.di_planos_entregas_id,
#                                                         di_planos_trabalho_id = entrega.di_planos_trabalho_id,
#                                                         di_avaliacao_id       = entrega.di_avaliacao_id,
#                                                         di_trabalhos_id       = entrega.di_trabalhos_id,
#                                                         di_tempo_ini_id       = entrega.di_tempo_ini_id,
#                                                         di_tempo_fim_id       = entrega.di_tempo_fim_id,
#                                                         data_inicio           = entrega.data_inicio,
#                                                         data_fim              = entrega.data_fim,
#                                                         descricao             = entrega.descricao,
#                                                         destinatario          = entrega.destinatario,
#                                                         meta                  = entrega.meta,
#                                                         entrega_id            = entrega.entrega_id,
#                                                         unidade_sigla         = entrega.unidade_sigla,
#                                                         unidade_nome          = entrega.unidade_nome,
#                                                         grupo_nome            = entrega.grupo_nome,
#                                                         grupo_desc            = entrega.grupo_desc)
#                     db.session.add(nova_tr_ft_entregas)
#                 db.session.commit() 
#                 ultimo_id = le_ft_entregas[-1].ft_entregas_id

#             # Limpa tabela ft_entregas
#             db.session.query(ft_entregas).delete()
#             db.session.commit()   

#             ultimo_id = 0
#             tamanho_lote = 200000
#             lote = 0

#             while True:
#                 lote += 1
#                 LOGGER.info(f'Processando lote {lote} na junção ft_entregas e di_trabalhos...')

#                 ft_entregas_trab = db.session.query(tr_ft_entregas.ft_entregas_id,
#                                                     tr_ft_entregas.entrega_id,
#                                                     di_trabalhos.di_trabalhos_id,
#                                                     tr_ft_entregas.di_usuarios_id,
#                                                     tr_ft_entregas.di_unidades_id,
#                                                     tr_ft_entregas.di_planos_entregas_id,
#                                                     tr_ft_entregas.di_planos_trabalho_id,
#                                                     tr_ft_entregas.di_avaliacao_id,
#                                                     tr_ft_entregas.di_tempo_ini_id,
#                                                     tr_ft_entregas.di_tempo_fim_id,
#                                                     tr_ft_entregas.data_inicio,
#                                                     tr_ft_entregas.data_fim,
#                                                     tr_ft_entregas.descricao,
#                                                     tr_ft_entregas.destinatario,
#                                                     tr_ft_entregas.meta,
#                                                     tr_ft_entregas.unidade_sigla,
#                                                     tr_ft_entregas.unidade_nome,
#                                                     tr_ft_entregas.grupo_nome, 
#                                                     tr_ft_entregas.grupo_desc)\
#                                             .outerjoin(di_trabalhos, tr_ft_entregas.entrega_id == di_trabalhos.entrega_id)\
#                                             .filter(tr_ft_entregas.ft_entregas_id > ultimo_id) \
#                                             .order_by(tr_ft_entregas.ft_entregas_id)\
#                                             .limit(tamanho_lote)\
#                                             .all()
#                 if not ft_entregas_trab:
#                     break            

#                 for item in ft_entregas_trab:

#                     registros += 1

#                     if item.di_trabalhos_id is None:
#                         tr_sk = -1
#                     else:   
#                         tr_sk = item.di_trabalhos_id
                        
#                     nova_ft_entrega = ft_entregas(di_trabalhos_id       = tr_sk,
#                                                   di_unidades_id        = item.di_unidades_id,
#                                                   di_usuarios_id        = item.di_usuarios_id,
#                                                   di_planos_entregas_id = item.di_planos_entregas_id,
#                                                   di_planos_trabalho_id = item.di_planos_trabalho_id,
#                                                   di_avaliacao_id       = item.di_avaliacao_id,
#                                                   di_tempo_ini_id       = item.di_tempo_ini_id,
#                                                   di_tempo_fim_id       = item.di_tempo_fim_id,
#                                                   data_inicio           = item.data_inicio,
#                                                   data_fim              = item.data_fim,
#                                                   descricao             = item.descricao,
#                                                   destinatario          = item.destinatario,
#                                                   meta                  = item.meta,
#                                                   entrega_id            = item.entrega_id,
#                                                   unidade_sigla         = item.unidade_sigla,
#                                                   unidade_nome          = item.unidade_nome,
#                                                   grupo_nome            = item.grupo_nome, 
#                                                   grupo_desc            = item.grupo_desc)
                
#                     db.session.add(nova_ft_entrega)
#                 db.session.commit()

#                 ultimo_id = ft_entregas_trab[-1].ft_entregas_id

#             LOGGER.info(f'ft_entregas conectada com di_trabalhos.')

#         LOGGER.info(f'Fato ft_entregas preenchida.')

#         end_time = time.perf_counter()
        
#         elapsed_time = (end_time - start_time)/60
#         LOGGER.info(f'Tempo total de carga da ft_entregas: {elapsed_time:.2f} minutos.')
#         LOGGER.info(f'...')


######################################
# Função para criar a ft_desempenho
###################################

def carga_ft_desempenho(*args):
    """ 
    Preenche a tabela fato ft_desempenho.
    """
    with app.app_context():
        
        start_time = time.perf_counter()

        if 'di_tempo' in args:

            # Limpa tabela ft_desempenho
            db.session.query(ft_desempenho).delete()
            db.session.commit()
            LOGGER.info(f'...')
            LOGGER.info(f'Fato ft_desempenho esvaziada.')

            LOGGER.info(f'Iniciando construção de ft_desempenho, já conectanto com di_tempo.')

    # Montando ft_desempenho a partir de di_trabalhos e juntando com di_tempo, usando data_distribuição como referência (pegando sk da dimensão)
    
            ft_desempenho_tempo = db.session.query(di_trabalhos.id,
                                                   di_trabalhos.di_trabalhos_id,
                                                   di_trabalhos.prazo,
                                                   di_trabalhos.tempo_utilizado,
                                                   label('di_tempo_dist_id', di_tempo.id)) \
                                    .join(di_tempo, cast(di_trabalhos.atividade_data_distribuicao, Date) == cast(di_tempo.db_data, Date)) \
                                    .all()
            
            LOGGER.info(f'  ft_entregas com di_tempo: {len(ft_desempenho_tempo)} registros.')
            for item in ft_desempenho_tempo:  # percorre os resultados do join e cria regisrtros na ft_desempenho, um a um.
                ## Aqui ft_desempenho é criada, pois recebe dados pela primeira vez
                nova_ft_desempenho = ft_desempenho(di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   di_unidades_id        = -1,
                                                   di_usuarios_id        = -1,
                                                   di_planos_entregas_id = -1,
                                                   di_planos_trabalho_id = -1,
                                                   di_avaliacao_id       = -1,
                                                   di_entregas_id        = -1,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
                
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho criada e conectada com di_tempo.')

    # ft_desempenho com di_unidades e di_usuarios

        if 'di_unidades_e_di_usuarios' in args:
            LOGGER.info(f'Iniciando ligação da ft_desempenho com di_unidades e di_usuarios.')
            # Juntando referência a usuarios e unidades (pegando chaves substitutas)
            desempenho_usu_unid = db.session.query(di_usuarios.di_usuarios_id,
                                                   di_unidades.di_unidades_id,
                                                   ft_desempenho.di_trabalhos_id,
                                                   ft_desempenho.di_tempo_dist_id,
                                                   ft_desempenho.di_planos_entregas_id,
                                                   ft_desempenho.di_planos_trabalho_id,
                                                   ft_desempenho.di_avaliacao_id,
                                                   ft_desempenho.di_entregas_id,
                                                   ft_desempenho.prazo,
                                                   ft_desempenho.tempo_utilizado)\
                                .join(di_trabalhos, di_trabalhos.di_trabalhos_id == ft_desempenho.di_trabalhos_id)\
                                .outerjoin(di_usuarios, di_usuarios.id == di_trabalhos.usuario_id)\
                                .outerjoin(di_unidades, di_unidades.id == di_trabalhos.unidade_id)\
                                .all()
            LOGGER.info(f'  ft_desempenho com di_unidades e di_usuarios: {len(desempenho_usu_unid)} registros.')

            # Limpa tabela ft_desempenho. Ela será recriada a partir da consulta acima
            db.session.query(ft_desempenho).delete()
            db.session.commit()

            for item in desempenho_usu_unid:  
                if item.di_unidades_id is None:
                    un_sk = -1
                else:   
                    un_sk = item.di_unidades_id

                if item.di_usuarios_id is None:
                    us_sk = -1
                else:   
                    us_sk = item.di_usuarios_id 

                nova_ft_desempenho = ft_desempenho(di_planos_trabalho_id = item.di_planos_trabalho_id,
                                                   di_planos_entregas_id = item.di_planos_entregas_id,
                                                   di_avaliacao_id       = item.di_avaliacao_id,
                                                   di_entregas_id        = item.di_entregas_id,
                                                   di_unidades_id        = un_sk,
                                                   di_usuarios_id        = us_sk,
                                                   di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
            
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho conectada com com di_unidades e di_usuarios.')

    # ft_desempenho com di_avaliacoes

        if 'di_avaliacoes' in args:
            # Juntando referência a avaliações (pegando chaves substitutas)
            LOGGER.info(f'Iniciando ligação da ft_desempenho com di_avaliacoes.')
            desempenho_aval = db.session.query(di_avaliacoes.di_avaliacao_id,
                                               ft_desempenho.di_usuarios_id,
                                               ft_desempenho.di_unidades_id,
                                               ft_desempenho.di_trabalhos_id,
                                               ft_desempenho.di_entregas_id,
                                               ft_desempenho.di_tempo_dist_id,
                                               ft_desempenho.di_planos_entregas_id,
                                               ft_desempenho.di_planos_trabalho_id,
                                               ft_desempenho.prazo,
                                               ft_desempenho.tempo_utilizado)\
                                .outerjoin(di_trabalhos, di_trabalhos.di_trabalhos_id == ft_desempenho.di_trabalhos_id)\
                                .outerjoin(di_avaliacoes, di_avaliacoes.id == di_trabalhos.avaliacao_id)\
                                .all()
            LOGGER.info(f'  ft_desempenho com di_avaliacoes: {len(desempenho_aval)} registros.')

            # Limpa tabela ft_desempenho. Ela será recriada a partir da consulta acima
            db.session.query(ft_desempenho).delete()
            db.session.commit()

            for item in desempenho_aval:  
                if item.di_avaliacao_id is None:
                    av_sk = -1
                else:   
                    av_sk = item.di_avaliacao_id

                nova_ft_desempenho = ft_desempenho(di_planos_trabalho_id = item.di_planos_trabalho_id,
                                                   di_planos_entregas_id = item.di_planos_entregas_id,
                                                   di_avaliacao_id       = av_sk,
                                                   di_entregas_id        = item.di_entregas_id,
                                                   di_unidades_id        = item.di_unidades_id,
                                                   di_usuarios_id        = item.di_usuarios_id,
                                                   di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
            
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho conectada com com di_avaliacoes.')

    # ft_desempenho com di_entregas

        if 'di_entregas' in args:
            # Juntando referência a entregas (pegando chaves substitutas)
            LOGGER.info(f'Iniciando ligação da ft_desempenho com di_entregas.')
            desempenho_entr = db.session.query(di_entregas.di_entregas_id,
                                               ft_desempenho.di_avaliacao_id,
                                               ft_desempenho.di_usuarios_id,
                                               ft_desempenho.di_unidades_id,
                                               ft_desempenho.di_trabalhos_id,
                                               ft_desempenho.di_tempo_dist_id,
                                               ft_desempenho.di_planos_entregas_id,
                                               ft_desempenho.di_planos_trabalho_id,
                                               ft_desempenho.prazo,
                                               ft_desempenho.tempo_utilizado)\
                                .outerjoin(di_trabalhos, di_trabalhos.di_trabalhos_id == ft_desempenho.di_trabalhos_id)\
                                .outerjoin(di_entregas, di_entregas.id == di_trabalhos.entrega_id)\
                                .all()
            LOGGER.info(f'  ft_desempenho com di_entregas: {len(desempenho_entr)} registros.')

            # Limpa tabela ft_desempenho. Ela será recriada a partir da consulta acima
            db.session.query(ft_desempenho).delete()
            db.session.commit()

            for item in desempenho_entr:  
                if item.di_entregas_id is None:
                    en_sk = -1
                else:   
                    en_sk = item.di_entregas_id

                nova_ft_desempenho = ft_desempenho(di_planos_trabalho_id = item.di_planos_trabalho_id,
                                                   di_planos_entregas_id = item.di_planos_entregas_id,
                                                   di_entregas_id        = en_sk,
                                                   di_avaliacao_id       = item.di_avaliacao_id,
                                                   di_unidades_id        = item.di_unidades_id,
                                                   di_usuarios_id        = item.di_usuarios_id,
                                                   di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
            
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho conectada com com di_entregas.')

    # ft_desempenho com di_planos_entregas

        if 'di_planos_entregas' in args:
            # Juntando referência a planos de entregas (pegando chaves substitutas)
            LOGGER.info(f'Iniciando ligação da ft_desempenho com di_planos_entregas.')
            desempenho_pe = db.session.query(di_planos_entregas.di_planos_entregas_id,
                                             ft_desempenho.di_avaliacao_id,
                                             ft_desempenho.di_usuarios_id,
                                             ft_desempenho.di_unidades_id,
                                             ft_desempenho.di_trabalhos_id,
                                             ft_desempenho.di_tempo_dist_id,
                                             ft_desempenho.di_entregas_id,
                                             ft_desempenho.di_planos_trabalho_id,
                                             ft_desempenho.prazo,
                                             ft_desempenho.tempo_utilizado)\
                                .outerjoin(di_entregas, di_entregas.di_entregas_id == ft_desempenho.di_entregas_id)\
                                .outerjoin(di_planos_entregas, di_planos_entregas.id == di_entregas.plano_entrega_id)\
                                .all()
            LOGGER.info(f'  ft_desempenho com di_planos_entregas: {len(desempenho_pe)} registros.')

            # Limpa tabela ft_desempenho. Ela será recriada a partir da consulta acima
            db.session.query(ft_desempenho).delete()
            db.session.commit()

            for item in desempenho_pe:  
                if item.di_planos_entregas_id is None:
                    pe_sk = -1
                else:   
                    pe_sk = item.di_planos_entregas_id

                nova_ft_desempenho = ft_desempenho(di_planos_trabalho_id = item.di_planos_trabalho_id,
                                                   di_planos_entregas_id = pe_sk,
                                                   di_entregas_id        = item.di_entregas_id,
                                                   di_avaliacao_id       = item.di_avaliacao_id,
                                                   di_unidades_id        = item.di_unidades_id,
                                                   di_usuarios_id        = item.di_usuarios_id,
                                                   di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
            
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho conectada com com di_planos_entregas.')

    # ft_desempenho com di_planos_trabalho

        if 'di_planos_trabalho' in args:
            # Juntando referência a planos de trabalho (pegando chaves substitutas)
            LOGGER.info(f'Iniciando ligação da ft_desempenho com di_planos_trabalho.')
            desempenho_pt = db.session.query(di_planos_trabalho.di_planos_trabalho_id,
                                             ft_desempenho.di_avaliacao_id,
                                             ft_desempenho.di_usuarios_id,
                                             ft_desempenho.di_unidades_id,
                                             ft_desempenho.di_trabalhos_id,
                                             ft_desempenho.di_tempo_dist_id,
                                             ft_desempenho.di_entregas_id,
                                             ft_desempenho.di_planos_entregas_id,
                                             ft_desempenho.prazo,
                                             ft_desempenho.tempo_utilizado)\
                                .outerjoin(di_trabalhos, di_trabalhos.di_trabalhos_id == ft_desempenho.di_trabalhos_id)\
                                .outerjoin(di_planos_trabalho, di_planos_trabalho.id == di_trabalhos.plano_trabalho_id)\
                                .all()
            LOGGER.info(f'  ft_desempenho com di_planos_trabalho: {len(desempenho_pt)} registros.')

            # Limpa tabela ft_desempenho. Ela será recriada a partir da consulta acima
            db.session.query(ft_desempenho).delete()
            db.session.commit()

            for item in desempenho_pt:  
                if item.di_planos_trabalho_id is None:
                    pt_sk = -1
                else:   
                    pt_sk = item.di_planos_trabalho_id

                nova_ft_desempenho = ft_desempenho(di_planos_trabalho_id = pt_sk,
                                                   di_planos_entregas_id = item.di_planos_entregas_id,
                                                   di_entregas_id        = item.di_entregas_id,
                                                   di_avaliacao_id       = item.di_avaliacao_id,
                                                   di_unidades_id        = item.di_unidades_id,
                                                   di_usuarios_id        = item.di_usuarios_id,
                                                   di_trabalhos_id       = item.di_trabalhos_id,
                                                   di_tempo_dist_id      = item.di_tempo_dist_id,
                                                   prazo                 = item.prazo,
                                                   tempo_utilizado       = item.tempo_utilizado)
            
                db.session.add(nova_ft_desempenho)  
            db.session.commit()
            LOGGER.info(f'  ft_desempenho conectada com com di_planos_trabalho.')


        end_time = time.perf_counter()
        
        elapsed_time = (end_time - start_time)/60
        LOGGER.info(f'Tempo total de carga da ft_desempenho: {elapsed_time:.2f} minutos.')
        LOGGER.info(f'...')


@dim_fat.route('/gera_dimensoes', methods=['GET', 'POST'])
def gera_dimensoes():
    """
    +---------------------------------------------------------------------------------------+
    |Gerando as tabelas de dimensão.                                                        |
    +---------------------------------------------------------------------------------------+
    """

    # Define o intervalo de datas para popular a di_tempo a partir de variáveis de ambiente
    data_ini = dt.strptime(os.environ.get('DATA_INI'),'%Y-%m-%d').date()
    data_fim = dt.strptime(os.environ.get('DATA_FIM'),'%Y-%m-%d').date()


    start_time = time.perf_counter()
    
    # Criando a di_tempo
    populando_di_tempo(data_ini, data_fim) 

    # Criando as dimensões
    
    carga_dimensoes()

    end_time = time.perf_counter()
    
    elapsed_time = (end_time - start_time)/60
    LOGGER.info(f'Tempo total de carga das tabelas dimensão: {elapsed_time:.2f} minutos.')

    flash('Tabelas de dimensão geradas com sucesso!','sucesso')

    return render_template ('index.html') 


@dim_fat.route('/gera_fatos/<ft>', methods=['GET', 'POST'])
def gera_fatos(ft):
    """
    +---------------------------------------------------------------------------------------+
    |Gerando as tabelas de fatos.                                                           |
    +---------------------------------------------------------------------------------------+
    """
   
    # if ft == 'ft_entregas':
    #     # Criando a ft_entregas em tread separado para agilizar o processo

    #     thr = Thread(target=carga_ft_entregas, args=('di_tempo',
    #                                                 'di_planos_entregas',
    #                                                 'di_unidades_e_di_usuarios',
    #                                                 'di_planos_trabalho',
    #                                                 'di_avaliacoes',))
    #     thr.start()   

    #     flash('ft_entregas será gerada em segundo plano!','info')

    if ft == 'ft_desempenho':
        # Criando a ft_desempenho em tread separado para agilizar o processo

        thr = Thread(target=carga_ft_desempenho, args=('di_tempo',
                                                       'di_unidades_e_di_usuarios',
                                                       'di_avaliacoes',
                                                       'di_entregas',
                                                       'di_planos_entregas',
                                                       'di_planos_trabalho',))
        thr.start()   

        flash('ft_desempenho será gerada em segundo plano!','info')    

    return render_template ('index.html') 

# @dim_fat.route('/fraciona_ft_entregas', methods=['GET', 'POST'])
# def fraciona_ft_entregas():
#     """
#     +---------------------------------------------------------------------------------------+
#     |Gerando as tabelas de fatos de forma fracioanda.                                       |
#     +---------------------------------------------------------------------------------------+
#     """
   
#     # Criando a ft_entregas em tread separado para agilizar o processo, permitindo uma dimensão por vez

#     form = FatoForm()

#     form.dimensao.choices = [
#                             ('di_tempo', 'di_tempo'),
#                             ('di_planos_entregas', 'di_planos_entregas'),
#                             ('di_unidades_e_di_usuarios', 'di_unidades_e_di_usuarios'),
#                             ('di_planos_trabalho', 'di_planos_trabalho'),
#                             ('di_avaliacoes', 'di_avaliacoes')
#                             ]   

#     if form.validate_on_submit():

#         dimensao = form.dimensao.data

#         thr = Thread(target=carga_ft_entregas, args=(dimensao,))
#         thr.start()   

#         flash('Fato sendo gerado fracionado em segundo plano!. '+'DI: '+ dimensao,'info')

#         return redirect(url_for('core.index'))

#     return render_template ('fraciona_ft_entregas.html', form=form)

