from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__,static_url_path='/static', static_folder='static')
app.config.from_object(Config)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login= LoginManager(app)
login.login_view = 'login'

if not app.debug:
    if app.config['MAIL_USERNAME'] or app.config['MAIL_PASSWORD']:
        auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
    secure = None
    if app.config['MAIL_USE_TLS']:
        secure = ()    
    mail_handler = SMTPHandler(
        mailhost=(app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD']),
        fromaddr='no-reply@' + str(app.config['MAIL_PORT']),
        toaddrs=app.config['ADMINS'], subject='Tinker full-stack Flask App Failure',
        credentials=auth, secure=secure)
    mail_handler.setLevel(logging.ERROR)
    app.logger.addHandler(mail_handler)

if not app.debug :
    if app.config['MAIL_SERVER']:
        pass

    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler(
        'logs/tinker_app.log',
        maxBytes=10240,
        backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Tinker Full-stack App')

from app import routes, models, errors