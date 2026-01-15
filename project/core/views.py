"""
.. topic:: Core (views)

    Este é o módulo inicial do sistema.

    Apresenta as telas de início, direcionando para as principais funções do sistema.

.. topic:: Ações relacionadas ao módulo

    * Tela inicial: index

"""

# core/views.py

from flask import render_template, Blueprint, url_for, flash, redirect, request
from project import db, app

from project.models import tr_entregas_grupos
from project.core.forms import GrupoForm_1, GrupoForm_2

from datetime import datetime as dt


core = Blueprint("core",__name__)

@core.route('/')
def index():
    """
    +---------------------------------------------------------------------------------------+
    |Ações quando o aplicativo é colocado no ar.                                            |
    +---------------------------------------------------------------------------------------+
    """
  
        
    return render_template ('index.html') 

@core.route('/inicio')
def inicio():
    """
    +---------------------------------------------------------------------------------------+
    |Apresenta a tela inicial do aplicativo.                                                |
    +---------------------------------------------------------------------------------------+
    """

    return render_template ('index.html')    

@core.route('/entregas_grupos', methods=['GET','POST'])
def entregas_grupos():
    """
    +---------------------------------------------------------------------------------------+
    |Definição de grupos para classificar entregas.                                         |
    +---------------------------------------------------------------------------------------+
    """

    grupos = db.session.query(tr_entregas_grupos)\
                        .order_by(tr_entregas_grupos.nome)\
                        .all()

    quantidade = len(grupos)
        
    form_1 = GrupoForm_1()
    form_2 = GrupoForm_2()
    
    if form_1.submit_1.name in request.form and form_1.validate_on_submit():
        
        novo_grupo = tr_entregas_grupos(nome = form_1.nome.data, 
                                        desc = form_1.desc.data,
                                        palavras_chave= form_1.palavras_chave.data) 
        
        db.session.add(novo_grupo)
        db.session.commit()

        flash ('Grupo inserido!','sucesso')
        
        return redirect (url_for("core.entregas_grupos")) 
    
    elif form_2.submit_2.name in request.form and form_2.validate_on_submit():

        grupo = db.session.query(tr_entregas_grupos)\
                            .filter_by(id = int(form_2.id_grupo.data))\
                            .first()
                        
        grupo.nome = form_2.nome.data
        grupo.desc = form_2.desc.data
        grupo.palavras_chave= form_2.palavras_chave.data
        
        db.session.commit()

        flash ('Grupo alterado!','sucesso')
        
        return redirect (url_for("core.entregas_grupos"))

    return render_template('entregas_grupos.html', grupos = grupos, quantidade=quantidade, form_1 = form_1, form_2 = form_2)

@core.route('/<grupo_id>/deleta_grupo', methods=['GET','POST'])
def deleta_grupo(grupo_id):
    """
    +---------------------------------------------------------------------------------------+
    |Deleta grupo.                                                                          |
    +---------------------------------------------------------------------------------------+
    """
    
    tr_entregas_grupos.query.filter_by(id = grupo_id).delete()
    
    db.session.commit()
        
    flash ('Grupo deletado!','sucesso')
    
    return redirect (url_for("core.entregas_grupos"))        







