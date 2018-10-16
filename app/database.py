from flask_migrate import Migrate
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app import application

engine = create_engine(application.config.get('SQLALCHEMY_DATABASE_URI'))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()
migrate = Migrate(application, Base)
