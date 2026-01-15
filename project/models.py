"""
.. topic:: Modelos (tabelas nos bancos de dados)

    Os modelos são classes que definem a estrutura das tabelas dos bancos de dados.

    Os modelos de interesse do banco petrvs_home são os seguintes:

    Área de Stage
    * st_unidades
    * st_usuarios
    * st_planos_entregas
    * st_planos_trabalho
    * st_entregas

"""
# models.py

from project import app
from project import db
from datetime import datetime, date
import os

######
##
##  S T A G E  A R E A
##
###################


# STAGE UNIDADES

class st_unidades(db.Model):

    __tablename__ = 'st_unidades'
    # __table_args__ = {"schema": "stage"}

    id              = db.Column(db.String, primary_key = True)
    sigla           = db.Column(db.String)
    nome            = db.Column(db.String)
    unidade_pai_id  = db.Column(db.String)
    uf              = db.Column(db.String)
    path            = db.Column(db.String)
    codigo          = db.Column(db.String)
    data_inativacao = db.Column(db.String)

    def __init__(self, id
                     , sigla
                     , nome
                     , unidade_pai_id
                     , uf
                     , path
                     , codigo
                     , data_inativacao):
        
        self.id              = id
        self.sigla           = sigla
        self.nome            = nome
        self.unidade_pai_id  = unidade_pai_id
        self.uf              = uf
        self.path            = path
        self.codigo          = codigo
        self.data_inativacao = data_inativacao


# STAGE USUÁRIOS

class st_usuarios(db.Model):

    __tablename__ = 'st_usuarios'
    # __table_args__ = {"schema": ""}
    
    id                       = db.Column(db.String, primary_key = True)
    nome                     = db.Column(db.String)
    email                    = db.Column(db.String)
    cpf                      = db.Column(db.String)
    matricula                = db.Column(db.String)
    data_nascimento          = db.Column(db.DateTime)
    uf                       = db.Column(db.String)
    sexo                     = db.Column(db.String)
    situacao_funcional       = db.Column(db.String)
    data_modificacao         = db.Column(db.DateTime)
    modalidade_pgd           = db.Column(db.String)
    participa_pgd            = db.Column(db.String)
    nome_jornada             = db.Column(db.String)
    cod_jornada              = db.Column(db.Integer)
    

    def __init__(self, id
                     , nome
                     , email
                     , cpf
                     , matricula
                     , data_nascimento
                     , uf
                     , sexo
                     , situacao_funcional
                     , data_modificacao
                     , modalidade_pgd
                     , participa_pgd
                     , nome_jornada
                     , cod_jornada):

        self.id                       = id
        self.email                    = email
        self.nome                     = nome
        self.cpf                      = cpf
        self.matricula                = matricula
        self.data_nascimento          = data_nascimento
        self.uf                       = uf
        self.sexo                     = sexo
        self.situacao_funcional       = situacao_funcional
        self.data_modificacao         = data_modificacao
        self.modalidade_pgd           = modalidade_pgd
        self.participa_pgd            = participa_pgd
        self.nome_jornada             = nome_jornada
        self.cod_jornada              = cod_jornada


# STAGE Planos de Entregas

class st_planos_entregas(db.Model):

    __tablename__ = 'st_planos_entregas'
    # __table_args__ = {"schema": ""}

    id                  = db.Column(db.String, primary_key = True)
    numero              = db.Column(db.Integer)
    data_inicio         = db.Column(db.DateTime)
    data_fim            = db.Column(db.DateTime)
    data_arquivamento   = db.Column(db.DateTime)
    nome                = db.Column(db.String)
    status              = db.Column(db.String)
    planejamento_id     = db.Column(db.String)
    cadeia_valor_id     = db.Column(db.String)
    unidade_id          = db.Column(db.String)
    programa_id         = db.Column(db.String)
    avaliacao_id        = db.Column(db.String)
    okr_id              = db.Column(db.String)

    def __init__(self, id
                     , numero
                     , data_inicio
                     , data_fim
                     , data_arquivamento
                     , nome
                     , status
                     , planejamento_id
                     , cadeia_valor_id
                     , unidade_id
                     , programa_id
                     , avaliacao_id
                     , okr_id):

        self.id                 = id
        self.numero             = numero
        self.data_inicio        = data_inicio
        self.data_fim           = data_fim 
        self.data_arquivamento  = data_arquivamento
        self.nome               = nome
        self.status             = status
        self.planejamento_id    = planejamento_id
        self.cadeia_valor_id    = cadeia_valor_id
        self.unidade_id         = unidade_id
        self.programa_id        = programa_id
        self.avaliacao_id       = avaliacao_id
        self.okr_id             = okr_id
        

# STAGE Planos de trabalho

class st_planos_trabalho(db.Model):

    __tablename__ = 'st_planos_trabalho'
    # __table_args__ = {"schema": ""}

    id                           = db.Column(db.String, primary_key = True)
    carga_horaria                = db.Column(db.Float)
    numero                       = db.Column(db.Integer)
    data_inicio                  = db.Column(db.DateTime)
    data_fim                     = db.Column(db.DateTime)
    forma_contagem_carga_horaria = db.Column(db.String)
    status                       = db.Column(db.String)
    programa_id                  = db.Column(db.String)
    usuario_id                   = db.Column(db.String)
    unidade_id                   = db.Column(db.String)
    tipo_modalidade_id           = db.Column(db.String)

    def __init__(self, id
                     , carga_horaria
                     , numero
                     , data_inicio
                     , data_fim
                     , forma_contagem_carga_horaria
                     , status
                     , programa_id
                     , usuario_id
                     , unidade_id
                     , tipo_modalidade_id):

        self.id                           = id
        self.carga_horaria                = carga_horaria
        self.numero                       = numero
        self.data_inicio                  = data_inicio
        self.data_fim                     = data_fim
        self.forma_contagem_carga_horaria = forma_contagem_carga_horaria
        self.status                       = status
        self.programa_id                  = programa_id
        self.usuario_id                   = usuario_id
        self.unidade_id                   = unidade_id
        self.tipo_modalidade_id           = tipo_modalidade_id

# STAGE Entregas dos Planos de Trabalho

class st_planos_trabalhos_entregas(db.Model):

    __tablename__ = 'st_planos_trabalhos_entregas'
    # __table_args__ = {"schema": ""}

    id                           = db.Column(db.String, primary_key = True)
    plano_trabalho_id            = db.Column(db.String)
    plano_entrega_entrega_id     = db.Column(db.String)

    def __init__(self, id
                     , plano_trabalho_id
                     , plano_entrega_entrega_id):
        
        self.id                        = id
        self.plano_trabalho_id         = plano_trabalho_id
        self.plano_entrega_entrega_id  = plano_entrega_entrega_id

# STAGE Entregas    

class st_entregas(db.Model):

    __tablename__ = 'st_entregas'
    # __table_args__ = {"schema": ""}

    id                  = db.Column(db.String, primary_key = True)
    homologado          = db.Column(db.Integer)
    progresso_esperado  = db.Column(db.Float)
    progresso_realizado = db.Column(db.Float)
    data_inicio         = db.Column(db.DateTime)
    data_fim            = db.Column(db.DateTime)
    descricao           = db.Column(db.String)
    destinatario        = db.Column(db.String)
    meta_tipo           = db.Column(db.String)
    meta_valor          = db.Column(db.String)
    realizado_tipo      = db.Column(db.String)
    realizado_valor     = db.Column(db.String)
    descricao_meta      = db.Column(db.String)
    descricao_entrega   = db.Column(db.String)
    plano_entrega_id    = db.Column(db.String)
    unidade_sigla       = db.Column(db.String)
    unidade_nome        = db.Column(db.String)
    unidade_id          = db.Column(db.String)
    grupo_nome          = db.Column(db.String)
    grupo_desc          = db.Column(db.String)

    def __init__(self, id
                        , homologado
                        , progresso_esperado
                        , progresso_realizado
                        , data_inicio
                        , data_fim
                        , descricao
                        , destinatario
                        , meta_tipo
                        , meta_valor
                        , realizado_tipo
                        , realizado_valor
                        , descricao_meta
                        , descricao_entrega
                        , plano_entrega_id
                        , unidade_sigla
                        , unidade_nome
                        , unidade_id
                        , grupo_nome
                        , grupo_desc):
    
            self.id                   = id
            self.homologado           = homologado
            self.progresso_esperado   = progresso_esperado
            self.progresso_realizado  = progresso_realizado
            self.data_inicio          = data_inicio 
            self.data_fim             = data_fim 
            self.descricao            = descricao
            self.destinatario         = destinatario
            self.meta_tipo            = meta_tipo
            self.meta_valor           = meta_valor
            self.realizado_tipo       = realizado_tipo
            self.realizado_valor      = realizado_valor
            self.descricao_meta       = descricao_meta
            self.descricao_entrega    = descricao_entrega
            self.plano_entrega_id     = plano_entrega_id
            self.unidade_sigla        = unidade_sigla
            self.unidade_nome         = unidade_nome  
            self.unidade_id           = unidade_id    
            self.grupo_nome           = grupo_nome
            self.grupo_desc           = grupo_desc

# STAGE Avaliações

class st_avaliacoes(db.Model):

    __tablename__ = 'st_avaliacoes'
    # __table_args__ = {"schema": ""}

    id                              = db.Column(db.String, primary_key = True)
    data_avaliacao                  = db.Column(db.DateTime)
    nota                            = db.Column(db.String)
    recurso                         = db.Column(db.String)
    data_recurso                    = db.Column(db.String)
    avaliador_nome                  = db.Column(db.String)
    tipo_avaliacao_nome             = db.Column(db.String)
    tipo_avaliacao_tipo             = db.Column(db.String)
    tipo_avaliacao_nota_descricao   = db.Column(db.String)
    plano_entrega_id                = db.Column(db.String)
    plano_trabalho_consolidacao_id  = db.Column(db.String)

    def __init__(self, id
                     , data_avaliacao
                     , nota
                     , recurso
                     , data_recurso
                     , avaliador_nome
                     , tipo_avaliacao_nome
                     , tipo_avaliacao_tipo
                     , tipo_avaliacao_nota_descricao
                     , plano_entrega_id
                     , plano_trabalho_consolidacao_id):

        self.id                 = id
        self.data_avaliacao     = data_avaliacao
        self.nota               = nota
        self.recurso            = recurso
        self.data_recurso       = data_recurso
        self.avaliador_nome     = avaliador_nome
        self.tipo_avaliacao_nome            = tipo_avaliacao_nome
        self.tipo_avaliacao_tipo            = tipo_avaliacao_tipo
        self.tipo_avaliacao_nota_descricao  = tipo_avaliacao_nota_descricao
        self.plano_entrega_id               = plano_entrega_id
        self.plano_trabalho_consolidacao_id = plano_trabalho_consolidacao_id

# STAGE Lotações

class st_lotacoes(db.Model):

    __tablename__ = 'st_lotacoes'
    # __table_args__ = {"schema": ""}

    id              = db.Column(db.String, primary_key = True)
    usuario_id      = db.Column(db.String)
    unidade_id      = db.Column(db.String)
    usuario_nome    = db.Column(db.String)
    unidade_sigla   = db.Column(db.String)
    unidade_nome    = db.Column(db.String)
    unidade_uf      = db.Column(db.String)

    def __init__(self, usuario_id
                     , unidade_id
                     , usuario_nome
                     , unidade_sigla
                     , unidade_nome
                     , unidade_uf):
        
        self.usuario_id    = usuario_id
        self.unidade_id    = unidade_id
        self.usuario_nome  = usuario_nome
        self.unidade_sigla = unidade_sigla
        self.unidade_nome  = unidade_nome
        self.unidade_uf    = unidade_uf

# stage Trabalhos (atividades, consolidações e avaliações)

class st_trabalhos(db.Model):

    __tablename__ = 'st_trabalhos'
    # __table_args__ = {"schema": ""}

    id                                  = db.Column(db.String, primary_key = True)
    atividade_descricao                 = db.Column(db.String)
    atividade_status                    = db.Column(db.String)
    tipo_atividade_nome                 = db.Column(db.String)
    plano_trabalho_consolidacao_status  = db.Column(db.String)
    avaliacao_id                        = db.Column(db.String)
    entrega_id                          = db.Column(db.String)
    atividade_data_distribuicao         = db.Column(db.DateTime)
    atividade_progresso                 = db.Column(db.Float)
    prazo                               = db.Column(db.Integer)
    tempo_utilizado                     = db.Column(db.Integer)
    usuario_id                          = db.Column(db.String)
    unidade_id                          = db.Column(db.String)
    plano_trabalho_id                   = db.Column(db.String)
    forca_trabalho                      = db.Column(db.Float)


    def __init__(self, atividade_descricao
                     , atividade_status
                     , tipo_atividade_nome
                     , plano_trabalho_consolidacao_status
                     , avaliacao_id
                     , entrega_id
                     , atividade_data_distribuicao
                     , atividade_progresso
                     , prazo
                     , tempo_utilizado
                     , usuario_id
                     , unidade_id
                     , plano_trabalho_id
                     , forca_trabalho):
        
        self.atividade_descricao                = atividade_descricao
        self.atividade_status                   = atividade_status
        self.tipo_atividade_nome                = tipo_atividade_nome
        self.plano_trabalho_consolidacao_status = plano_trabalho_consolidacao_status
        self.avaliacao_id                       = avaliacao_id
        self.entrega_id                         = entrega_id
        self.atividade_data_distribuicao        = atividade_data_distribuicao
        self.atividade_progresso                = atividade_progresso
        self.prazo                              = prazo
        self.tempo_utilizado                    = tempo_utilizado
        self.usuario_id                         = usuario_id
        self.unidade_id                         = unidade_id
        self.plano_trabalho_id                  = plano_trabalho_id
        self.forca_trabalho                     = forca_trabalho


######
##
##  D I M E S S Õ E S  E  F A T O S
##
###################

class di_tempo(db.Model):

    __tablename__ = 'di_tempo'

    id                  = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    db_data             = db.Column(db.Date, unique=True, nullable=False)
    ano                 = db.Column(db.Integer, nullable=False)
    mes                 = db.Column(db.Integer, nullable=False)
    dia                 = db.Column(db.Integer, nullable=False)
    quinzena            = db.Column(db.Integer, nullable=False)
    semana              = db.Column(db.Integer, nullable=False)
    dia_semana          = db.Column(db.String, nullable=False)
    mes_nome            = db.Column(db.String, nullable=False)
    final_de_semana     = db.Column(db.Boolean, default=False, nullable=False)
    feriado             = db.Column(db.Boolean, default=False, nullable=False)
    bimestre            = db.Column(db.Integer, nullable=False)
    nome_bimestre       = db.Column(db.String, nullable=False)
    trimestre           = db.Column(db.Integer, nullable=False)
    nome_trimestre      = db.Column(db.String, nullable=False)
    quadrimestre        = db.Column(db.Integer, nullable=False)
    nome_quadrimestre   = db.Column(db.String, nullable=False)
    semestre            = db.Column(db.Integer, nullable=False)
    nome_semestre       = db.Column(db.String, nullable=False)

    def __init__(self, db_data
                     , ano
                     , mes
                     , dia
                     , quinzena
                     , semana
                     , dia_semana
                     , mes_nome
                     , final_de_semana
                     , feriado
                     , bimestre
                     , nome_bimestre
                     , trimestre
                     , nome_trimestre
                     , quadrimestre
                     , nome_quadrimestre
                     , semestre
                     , nome_semestre):
        
        self.db_data            = db_data
        self.ano                = ano
        self.mes                = mes
        self.dia                = dia
        self.quinzena           = quinzena
        self.semana             = semana
        self.dia_semana         = dia_semana
        self.mes_nome           = mes_nome
        self.final_de_semana    = final_de_semana
        self.feriado            = feriado
        self.bimestre           = bimestre
        self.nome_bimestre      = nome_bimestre
        self.trimestre          = trimestre
        self.nome_trimestre     = nome_trimestre
        self.quadrimestre       = quadrimestre
        self.nome_quadrimestre  = nome_quadrimestre
        self.semestre           = semestre
        self.nome_semestre      = nome_semestre
        
    def __repr__(self):
        return f"<di_tempo (data='{self.db_data}')>"
    
class di_planos_entregas(db.Model):

    __tablename__ = 'di_planos_entregas'

    di_planos_entregas_id = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id                    = db.Column(db.String)
    nome                  = db.Column(db.String)
    numero                = db.Column(db.Integer)
    data_inicio           = db.Column(db.DateTime)
    data_fim              = db.Column(db.DateTime)
    data_arquivamento     = db.Column(db.DateTime)
    status                = db.Column(db.String)

    def __init__(self, id
                     , nome
                     , numero
                     , data_inicio
                     , data_fim
                     , data_arquivamento
                     , status):
        
        self.id                     = id
        self.nome                   = nome
        self.numero                 = numero
        self.data_inicio            = data_inicio
        self.data_fim               = data_fim
        self.data_arquivamento      = data_arquivamento
        self.status                 = status


class di_planos_trabalho(db.Model):

    __tablename__ = 'di_planos_trabalho'

    di_planos_trabalho_id        = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id                           = db.Column(db.String)
    numero                       = db.Column(db.Integer)
    carga_horaria                = db.Column(db.Float)
    data_inicio                  = db.Column(db.DateTime)
    data_fim                     = db.Column(db.DateTime)
    forma_contagem_carga_horaria = db.Column(db.String)
    status                       = db.Column(db.String)

    def __init__(self, id
                     , numero
                     , carga_horaria
                     , data_inicio
                     , data_fim
                     , forma_contagem_carga_horaria
                     , status):
        
        self.id                           = id
        self.numero                       = numero
        self.carga_horaria                = carga_horaria
        self.data_inicio                  = data_inicio
        self.data_fim                     = data_fim
        self.forma_contagem_carga_horaria = forma_contagem_carga_horaria
        self.status                       = status

    
class di_usuarios(db.Model):

    __tablename__ = 'di_usuarios'

    di_usuarios_id           = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id                       = db.Column(db.String)
    nome                     = db.Column(db.String)
    email                    = db.Column(db.String)
    cpf                      = db.Column(db.String)
    matricula                = db.Column(db.String)
    data_nascimento          = db.Column(db.DateTime)
    uf                       = db.Column(db.String)
    sexo                     = db.Column(db.String)
    situacao_funcional       = db.Column(db.String)
    data_modificacao         = db.Column(db.DateTime)
    modalidade_pgd           = db.Column(db.String)
    participa_pgd            = db.Column(db.String)
    nome_jornada             = db.Column(db.String)
    cod_jornada              = db.Column(db.Integer)

    def __init__(self, id
                     , nome
                     , email
                     , cpf
                     , matricula
                     , data_nascimento
                     , uf
                     , sexo
                     , situacao_funcional
                     , data_modificacao
                     , modalidade_pgd
                     , participa_pgd
                     , nome_jornada
                     , cod_jornada):

        self.id                       = id
        self.email                    = email
        self.nome                     = nome
        self.cpf                      = cpf
        self.matricula                = matricula
        self.data_nascimento          = data_nascimento
        self.uf                       = uf
        self.sexo                     = sexo
        self.situacao_funcional       = situacao_funcional
        self.data_modificacao         = data_modificacao
        self.modalidade_pgd           = modalidade_pgd
        self.participa_pgd            = participa_pgd
        self.nome_jornada             = nome_jornada
        self.cod_jornada              = cod_jornada


class di_unidades(db.Model):

    __tablename__ = 'di_unidades'

    di_unidades_id  = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id              = db.Column(db.String)
    sigla           = db.Column(db.String)
    nome            = db.Column(db.String)
    unidade_pai_id  = db.Column(db.String)
    uf              = db.Column(db.String)
    path            = db.Column(db.String)
    codigo          = db.Column(db.String)
    data_inativacao = db.Column(db.DateTime)

    def __init__(self, id
                     , sigla
                     , nome
                     , unidade_pai_id
                     , uf
                     , path
                     , codigo
                     , data_inativacao):
        
        self.id              = id
        self.sigla           = sigla
        self.nome            = nome
        self.unidade_pai_id  = unidade_pai_id
        self.uf              = uf
        self.path            = path
        self.codigo          = codigo
        self.data_inativacao = data_inativacao

class di_avaliacoes(db.Model):

    __tablename__ = "di_avaliacoes"

    di_avaliacao_id  = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id               = db.Column(db.String)
    data_avaliacao                  = db.Column(db.DateTime)
    nota                            = db.Column(db.String)
    recurso                         = db.Column(db.String)
    data_recurso                    = db.Column(db.DateTime)
    avaliador_nome                  = db.Column(db.String)
    tipo_avaliacao_nome             = db.Column(db.String)
    tipo_avaliacao_tipo             = db.Column(db.String)
    tipo_avaliacao_nota_descricao   = db.Column(db.String)
    plano_entrega_id                = db.Column(db.String)
    plano_trabalho_consolidacao_id  = db.Column(db.String)

    def __init__(self, id
                     , data_avaliacao
                     , nota
                     , recurso
                     , data_recurso
                     , avaliador_nome
                     , tipo_avaliacao_nome
                     , tipo_avaliacao_tipo
                     , tipo_avaliacao_nota_descricao
                     , plano_entrega_id
                     , plano_trabalho_consolidacao_id):
        
        self.id                 = id
        self.data_avaliacao     = data_avaliacao
        self.nota               = nota
        self.recurso            = recurso
        self.data_recurso       = data_recurso
        self.avaliador_nome     = avaliador_nome
        self.tipo_avaliacao_nome            = tipo_avaliacao_nome
        self.tipo_avaliacao_tipo            = tipo_avaliacao_tipo
        self.tipo_avaliacao_nota_descricao  = tipo_avaliacao_nota_descricao
        self.plano_entrega_id               = plano_entrega_id
        self.plano_trabalho_consolidacao_id = plano_trabalho_consolidacao_id    

class di_trabalhos(db.Model):

    __tablename__ = 'di_trabalhos'
    # __table_args__ = {"schema": ""}

    di_trabalhos_id                     = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id                                  = db.Column(db.String)
    atividade_descricao                 = db.Column(db.String)
    atividade_status                    = db.Column(db.String)
    tipo_atividade_nome                 = db.Column(db.String)
    plano_trabalho_consolidacao_status  = db.Column(db.String)
    avaliacao_id                        = db.Column(db.String)
    entrega_id                          = db.Column(db.String) 
    atividade_data_distribuicao         = db.Column(db.DateTime)
    atividade_progresso                 = db.Column(db.Float)
    prazo                               = db.Column(db.Integer)
    tempo_utilizado                     = db.Column(db.Integer)
    usuario_id                          = db.Column(db.String)
    unidade_id                          = db.Column(db.String)
    plano_trabalho_id                   = db.Column(db.String)
    forca_trabalho                      = db.Column(db.Float)

    def __init__(self, id
                     , atividade_descricao
                     , atividade_status
                     , tipo_atividade_nome
                     , plano_trabalho_consolidacao_status
                     , avaliacao_id
                     , entrega_id
                     , atividade_data_distribuicao
                     , atividade_progresso
                     , prazo
                     , tempo_utilizado
                     , usuario_id
                     , unidade_id
                     , plano_trabalho_id
                     , forca_trabalho):

        self.id                                 = id
        self.atividade_descricao                = atividade_descricao
        self.atividade_status                   = atividade_status
        self.tipo_atividade_nome                = tipo_atividade_nome
        self.plano_trabalho_consolidacao_status = plano_trabalho_consolidacao_status
        self.avaliacao_id                       = avaliacao_id
        self.entrega_id                         = entrega_id
        self.atividade_data_distribuicao        = atividade_data_distribuicao
        self.atividade_progresso                = atividade_progresso
        self.prazo                              = prazo
        self.tempo_utilizado                    = tempo_utilizado
        self.usuario_id                         = usuario_id
        self.unidade_id                         = unidade_id
        self.plano_trabalho_id                  = plano_trabalho_id
        self.forca_trabalho                     = forca_trabalho    


class di_entregas(db.Model):

    __tablename__ = 'di_entregas'
    # __table_args__ = {"schema": ""}

    di_entregas_id      = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    id                  = db.Column(db.String)
    homologado          = db.Column(db.Integer)
    progresso_esperado  = db.Column(db.Float)
    progresso_realizado = db.Column(db.Float)
    data_inicio         = db.Column(db.DateTime)
    data_fim            = db.Column(db.DateTime)
    descricao           = db.Column(db.String)
    destinatario        = db.Column(db.String)
    meta_tipo           = db.Column(db.String)
    meta_valor          = db.Column(db.String)
    realizado_tipo      = db.Column(db.String)
    realizado_valor     = db.Column(db.String)
    descricao_meta      = db.Column(db.String)
    descricao_entrega   = db.Column(db.String)
    plano_entrega_id    = db.Column(db.String)
    unidade_sigla       = db.Column(db.String)
    unidade_nome        = db.Column(db.String)
    unidade_id          = db.Column(db.String)
    grupo_nome          = db.Column(db.String)
    grupo_desc          = db.Column(db.String)

    def __init__(self, id
                        , homologado
                        , progresso_esperado
                        , progresso_realizado
                        , data_inicio
                        , data_fim
                        , descricao
                        , destinatario
                        , meta_tipo
                        , meta_valor
                        , realizado_tipo
                        , realizado_valor
                        , descricao_meta
                        , descricao_entrega
                        , plano_entrega_id
                        , unidade_sigla
                        , unidade_nome
                        , unidade_id
                        , grupo_nome
                        , grupo_desc):
    
            self.id                   = id
            self.homologado           = homologado
            self.progresso_esperado   = progresso_esperado
            self.progresso_realizado  = progresso_realizado
            self.data_inicio          = data_inicio 
            self.data_fim             = data_fim 
            self.descricao            = descricao
            self.destinatario         = destinatario
            self.meta_tipo            = meta_tipo
            self.meta_valor           = meta_valor
            self.realizado_tipo       = realizado_valor
            self.realizado_valor      = realizado_valor
            self.descricao_meta       = descricao_meta
            self.descricao_entrega    = descricao_entrega
            self.plano_entrega_id     = plano_entrega_id
            self.unidade_sigla        = unidade_sigla
            self.unidade_nome         = unidade_nome
            self.unidade_id           = unidade_id      
            self.grupo_nome           = grupo_nome
            self.grupo_desc           = grupo_desc


class ft_entregas(db.Model):

    __tablename__ = 'ft_entregas'

    ft_entregas_id        = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    di_unidades_id        = db.Column(db.Integer)
    di_usuarios_id        = db.Column(db.Integer)
    di_planos_entregas_id = db.Column(db.Integer)
    di_planos_trabalho_id = db.Column(db.Integer)
    di_avaliacao_id       = db.Column(db.Integer)
    di_trabalhos_id       = db.Column(db.Integer)
    di_tempo_ini_id       = db.Column(db.Integer)
    di_tempo_fim_id       = db.Column(db.Integer)
    data_inicio           = db.Column(db.DateTime)
    data_fim              = db.Column(db.DateTime)
    descricao             = db.Column(db.String)
    destinatario          = db.Column(db.String)
    meta                  = db.Column(db.String)
    entrega_id            = db.Column(db.String)
    unidade_sigla         = db.Column(db.String)
    unidade_nome          = db.Column(db.String)
    grupo_nome            = db.Column(db.String)
    grupo_desc            = db.Column(db.String)


    def __init__(self, di_unidades_id
                     , di_usuarios_id
                     , di_planos_entregas_id
                     , di_planos_trabalho_id
                     , di_avaliacao_id
                     , di_trabalhos_id
                     , di_tempo_ini_id
                     , di_tempo_fim_id   
                     , data_inicio
                     , data_fim
                     , descricao
                     , destinatario
                     , meta
                     , entrega_id
                     , unidade_sigla
                     , unidade_nome
                     , grupo_nome
                     , grupo_desc):
                     
        self.di_unidades_id        = di_unidades_id
        self.di_usuarios_id        = di_usuarios_id
        self.di_planos_entregas_id = di_planos_entregas_id
        self.di_planos_trabalho_id = di_planos_trabalho_id
        self.di_avaliacao_id       = di_avaliacao_id
        self.di_trabalhos_id       = di_trabalhos_id
        self.di_tempo_ini_id       = di_tempo_ini_id
        self.di_tempo_fim_id       = di_tempo_fim_id
        self.data_inicio           = data_inicio
        self.data_fim              = data_fim
        self.descricao             = descricao
        self.destinatario          = destinatario
        self.meta                  = meta
        self.entrega_id            = entrega_id
        self.unidade_sigla         = unidade_sigla
        self.unidade_nome          = unidade_nome
        self.grupo_nome            = grupo_nome
        self.grupo_desc            = grupo_desc


class ft_desempenho(db.Model):

    __tablename__ = 'ft_desempenho'

    ft_desempenho_id      = db.Column(db.Integer, primary_key=True, autoincrement=True)
    di_trabalhos_id       = db.Column(db.Integer) 
    di_unidades_id        = db.Column(db.Integer)
    di_usuarios_id        = db.Column(db.Integer)
    di_planos_entregas_id = db.Column(db.Integer)
    di_planos_trabalho_id = db.Column(db.Integer)
    di_avaliacao_id       = db.Column(db.Integer)
    di_entregas_id        = db.Column(db.Integer)
    di_tempo_dist_id      = db.Column(db.Integer)
    prazo                 = db.Column(db.Integer)
    tempo_utilizado       = db.Column(db.Integer)


    def __init__(self, di_trabalhos_id 
                     , di_unidades_id
                     , di_usuarios_id
                     , di_planos_entregas_id
                     , di_planos_trabalho_id
                     , di_avaliacao_id
                     , di_entregas_id
                     , di_tempo_dist_id
                     , prazo
                     , tempo_utilizado):
                     
        self.di_trabalhos_id       = di_trabalhos_id
        self.di_unidades_id        = di_unidades_id
        self.di_usuarios_id        = di_usuarios_id
        self.di_planos_entregas_id = di_planos_entregas_id
        self.di_planos_trabalho_id = di_planos_trabalho_id
        self.di_avaliacao_id       = di_avaliacao_id
        self.di_entregas_id        = di_entregas_id
        self.di_tempo_dist_id      = di_tempo_dist_id
        self.prazo                 = prazo
        self.tempo_utilizado       = tempo_utilizado




# Tabelas de trabalho

class tr_entregas_palavras(db.Model):
    __tablename__ = 'tr_entregas_palavras'

    id      = db.Column(db.Integer, primary_key=True) 
    palavra = db.Column(db.String)

    def __init__(self, palavra):
        
        self.palavra = palavra

class tr_entregas_grupos(db.Model):
    __tablename__ = 'tr_entregas_grupos'

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True) 
    nome            = db.Column(db.String)
    desc            = db.Column(db.String)
    palavras_chave  = db.Column(db.Text)

    def __init__(self, nome
                     , desc
                     , palavras_chave):
        
        self.nome = nome
        self.desc = desc
        self.palavras_chave = palavras_chave

class tr_ft_entregas(db.Model):

    __tablename__ = 'tr_ft_entregas'

    ft_entregas_id        = db.Column(db.Integer, primary_key=True) 
    di_unidades_id        = db.Column(db.Integer)
    di_usuarios_id        = db.Column(db.Integer)
    di_planos_entregas_id = db.Column(db.Integer)
    di_planos_trabalho_id = db.Column(db.Integer)
    di_avaliacao_id       = db.Column(db.Integer)
    di_trabalhos_id       = db.Column(db.Integer)
    di_tempo_ini_id       = db.Column(db.Integer)
    di_tempo_fim_id       = db.Column(db.Integer)
    data_inicio           = db.Column(db.DateTime)
    data_fim              = db.Column(db.DateTime)
    descricao             = db.Column(db.String)
    destinatario          = db.Column(db.String)
    meta                  = db.Column(db.String)
    entrega_id            = db.Column(db.String)
    unidade_sigla         = db.Column(db.String)
    unidade_nome          = db.Column(db.String)
    grupo_nome            = db.Column(db.String)
    grupo_desc            = db.Column(db.String)


    def __init__(self, ft_entregas_id
                     , di_unidades_id
                     , di_usuarios_id
                     , di_planos_entregas_id
                     , di_planos_trabalho_id
                     , di_avaliacao_id
                     , di_trabalhos_id
                     , di_tempo_ini_id
                     , di_tempo_fim_id   
                     , data_inicio
                     , data_fim
                     , descricao
                     , destinatario
                     , meta
                     , entrega_id
                     , unidade_sigla
                     , unidade_nome
                     , grupo_nome
                     , grupo_desc):
                     
        self.ft_entregas_id       = ft_entregas_id  
        self.di_unidades_id        = di_unidades_id
        self.di_usuarios_id        = di_usuarios_id
        self.di_planos_entregas_id = di_planos_entregas_id
        self.di_planos_trabalho_id = di_planos_trabalho_id
        self.di_avaliacao_id       = di_avaliacao_id
        self.di_trabalhos_id       = di_trabalhos_id
        self.di_tempo_ini_id       = di_tempo_ini_id
        self.di_tempo_fim_id       = di_tempo_fim_id
        self.data_inicio           = data_inicio
        self.data_fim              = data_fim
        self.descricao             = descricao
        self.destinatario          = destinatario
        self.meta                  = meta
        self.entrega_id            = entrega_id
        self.unidade_sigla         = unidade_sigla
        self.unidade_nome          = unidade_nome
        self.grupo_nome            = grupo_nome
        self.grupo_desc            = grupo_desc
