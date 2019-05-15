# all the imports
import sqlite3
import os
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from flask_security import Security, SQLAlchemyUserDatastore, \
    UserMixin, RoleMixin, login_required, current_user
from flask_security.utils import encrypt_password
import flask_admin
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from config import Config
from contextlib import closing
import logging
import logging.handlers as logHandler

from sqlalchemy import Column, String, create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy
from pprint import pprint

LOG_PATH = 'logs'
LOG_FILE = 'flask.log'

app = Flask(__name__)

app.config.from_object(Config)
pprint(app.config)

from database import db_session,db

db.init_app(app)

def connect_db():
    #pprint(os.path.abspath(app.config['DATABASE']))
    return sqlite3.connect(app.config['DATABASE'])

@app.before_request
def before_request():
    logUserinfo(request)
    pass

@app.teardown_request
def teardown_request(exception):
    #g.db.close()
    pass

from fh import fh as fh_blueprint
from api_v1 import api as api_blueprint

app.register_blueprint(fh_blueprint,url_prefix="/")
app.register_blueprint(api_blueprint,url_prefix="/hashcode/api")

jinja_environ = app.create_jinja_environment()
jinja_environ.globals['Config'] = app.config

def presetLogger():
    if os.path.exists(LOG_PATH):
        pass
    else:
        os.mkdir(LOG_PATH)

    #handler = logging.FileHandler("%s/%s" % (LOG_PATH, LOG_FILE), encoding='UTF-8')
    handler = logHandler.RotatingFileHandler("%s/%s" % (LOG_PATH, LOG_FILE),
        encoding='UTF-8', maxBytes=1024*1024,backupCount=40)
    logging_format = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s :\r\n %(message)s')
    handler.setFormatter(logging_format)
    app.logger.addHandler(handler)

def logUserinfo(request):
    if request.url.find("static/") < 0:
        app.logger.info("%s : %s", request.remote_addr, request.url)
        app.logger.info(request.user_agent)


from models.auth import *
# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

from models import Models
from madmin import UserView
app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'

admin = Admin(app, name='Error', template_mode='bootstrap3')
admin.add_view(UserView.HashView(Models.SearchHash, db.session))
#admin.add_view(UserView.HashView(Role, db.session))
#admin.add_view(UserView.HashView(User, db.session))
# define a context processor for merging flask-admin's template context into the
# flask-security views.
@security.context_processor
def security_context_processor():
    return dict(
        admin_base_template=admin.base_template,
        admin_view=admin.index_view,
        h=admin_helpers,
        get_url=url_for
    )

presetLogger()

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
