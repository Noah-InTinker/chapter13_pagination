from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler
import os

app = Flask(__name__)
app.config.from_object(Config)

# Objects
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login =LoginManager(app)

#Email logs

if not app.debug:
    if app.config['MAIL_SERVER']:
        auth = None
        if app.config['MAIL_USERNAME'] or app.config ['MAIL_PASSWORD']:
            auth = (app.config['MAIL_USERNAME'], app.config['MAIL_PASSWORD'])
        secure = None
        if app.config['MAIL_USE_TLS']:
            secure = ()
        mail_handler = SMTPHandler(
            mailhost=(app.config['MAIL_SERVER'], app.config['MAIL_PORT']),
            fromaddr='no-reply@' + app.config['MAIL_SERVER'],
            toaddrs=app.config['ADMINS'], subject='Tinker Full-stack Flask App Failure',
            credentials=auth, secure=secure)
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)
    #---------------
    #Logging to a file
    #---------------

    #Save logs to an existing folder called 'logs'
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

###Atempt to add color

# @app.after_request
# def log_response(response):
#     # Get the status code and the URL of the request that just happened
#     status_code = response.status_code
#     url = request.path # Note: ensure 'from flask import request' is at the top of your file
    
#     message = f"HTTP {status_code} - {url}"
    
#     if 200 <= status_code < 300:
#         app.logger.info(message)    # Writes INFO -> Green in VS Code
#     elif 300 <= status_code < 400:
#         app.logger.warning(message) # Writes WARNING -> Yellow in VS Code
#     elif 400 <= status_code < 600:
#         app.logger.error(message)   # Writes ERROR -> Red in VS Code
#     else:
#         app.logger.debug(message)
    
#     return response



from app import routes, models, errors