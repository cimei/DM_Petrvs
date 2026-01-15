"""
.. topic:: **dim_fat (formulários)**

    Os formulários do módulo *dim_fat*.

    * FatoForm: escolher dimensão para relacionar com a fato entregas.

"""

# forms.py na pasta core

from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField


class FatoForm(FlaskForm):
    
    dimensao = SelectField('Dimensão')
        
    submit = SubmitField('Executar') 
       
    
