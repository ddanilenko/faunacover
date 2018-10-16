from flask import Flask

from app.config import Config


application = Flask(__name__)
application.config.from_object(Config)


from app.rest_api import api
