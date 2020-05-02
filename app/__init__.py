import os

from flask import Flask
from app.models import db

# create and configure the app
app = Flask(__name__, instance_relative_config=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sanium.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
)

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
