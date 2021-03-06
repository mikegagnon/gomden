import flask
from flask import *
from flask_sslify import SSLify
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail, Message
from celery import Celery

import json
import time
from urllib.parse import unquote
import random
import string
import os

import config
from flask_simple_captcha import CAPTCHA

from core_gomden.core_gomden import core_gomden_blueprint, init as initCore
from landing.landing import landing_blueprint
from account.account import account_blueprint, init as initAccount



app = Flask(__name__, static_url_path="/static")
sslify = SSLify(app)

app.register_blueprint(core_gomden_blueprint)
app.register_blueprint(landing_blueprint)
app.register_blueprint(account_blueprint)

app.config["SECRET_KEY"] = config.SECRET_KEY

csrf = CSRFProtect(app)

from flask_mail import  Message
from celery import Celery

celery = Celery(app, broker=config.REDIS_URL)


CAPTCHA = CAPTCHA(config=config.CAPTCHA_CONFIG)
app = CAPTCHA.init_app(app)

# TODO: rm/simplify print-based logging
@celery.task()
def send_email(subject, sender, recipient, body):
    print("1 Sending email to " + recipient)
    with app.app_context():

        with mail.connect() as connection:
            msg = Message(
                subject,
                sender=sender,
                recipients=[recipient])
            msg.body = body
            print("2 Sending email to " + recipient)
            connection.send(msg)
            print("3 Sending email to " + recipient)

app.config.update(
    MAIL_SERVER=config.FLASK_EMAIL_SERVER,
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME=config.NOREPLY_EMAIL,
    MAIL_PASSWORD=config.FLASK_EMAIL_PASSWORD
    )

mail = Mail(app)

initAccount(app, send_email, CAPTCHA)
initCore(send_email, CAPTCHA)
