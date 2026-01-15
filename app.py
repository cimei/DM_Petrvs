from project import app
from flask import render_template
import os

@app.template_filter('retorna_var_amb')
def retorna_var_amb(chave):
    return os.getenv(chave)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
    app.run(port = 5013)