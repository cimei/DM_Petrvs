"""
.. topic:: **core (formulários)**

    Os formulários do módulo *core*.

    * ObjetivoForm: inserir novo grupo.

"""

# forms.py na pasta core

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField
from wtforms.validators import DataRequired


class GrupoForm_1(FlaskForm):
    
    nome = StringField('Nome', validators=[DataRequired(message="Informe um nome!")])
    desc = StringField('Descrição', validators=[DataRequired(message="Informe a descrição!")])
    palavras_chave = TextAreaField('Palavras_chave', validators=[DataRequired(message="Informe, pelo menos uma, palavra_chave!")])
        
    submit_1 = SubmitField('Registrar') 

class GrupoForm_2(FlaskForm):
    
    id_grupo        = StringField('id_grupo')
    nome            = StringField('Nome', validators=[DataRequired(message="Informe um nome!")])
    desc            = StringField('Descrição', validators=[DataRequired(message="Informe a descrição!")])
    palavras_chave  = TextAreaField('Palavras_chave', validators=[DataRequired(message="Informe, pelo menos uma, palavra_chave!")])
        
    submit_2 = SubmitField('Alterar')         
    
