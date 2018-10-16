from flask import Flask
from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import Config


Base = declarative_base()
migrate = Migrate()


def create_app(config_class=Config):
    application = Flask(__name__)
    application.config.from_object(config_class)
    application.engine = create_engine(config_class.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=application.engine)
    application.session = Session()
    migrate.init_app(application, Base)

    return application
