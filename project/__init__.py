import os
import locale
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


TOP_LEVEL_DIR = os.path.abspath(os.curdir)

app = Flask (__name__, static_url_path=None, instance_relative_config=True, static_folder='/app/project/static')

app.config.from_pyfile('flask.cfg')

app.static_url_path=app.config.get('STATIC_PATH')

db = SQLAlchemy(app)

Migrate(app, db)

locale.setlocale( locale.LC_ALL, '' )

############################################
## blueprints - registros

from project.core.views import core
from project.stage.views import stage
from project.dim_fat.views import dim_fat
from project.error_pages.handlers import error_pages

app.register_blueprint(core)
app.register_blueprint(stage)
app.register_blueprint(dim_fat)
app.register_blueprint(error_pages)
