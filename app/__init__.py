import os

from flask import Flask
from app.models import db
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore


class Config(object):
    SECRET_KEY = 'dev',

    SQLALCHEMY_DATABASE_URI = 'sqlite:///sanium.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SCHEDULER_JOBSTORES = {
        'default': SQLAlchemyJobStore(url='sqlite:///app/sanium.db')
    }

    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }

    SCHEDULER_JOB_DEFAULTS = {
        'coalesce': False,
        'max_instances': 3
    }

    SCHEDULER_API_ENABLED = True


app = Flask(__name__, instance_relative_config=True)
app.config.from_object(Config())

db.init_app(app)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

with app.app_context():
    from . import models, controllers, services

    db.create_all()
    models.init_app(app)
    controllers.init_app(app)
    services.init_app(app)
