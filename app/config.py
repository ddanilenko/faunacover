import os


class Config:
    DB_USER = "postgres"
    DB_USER_PASSWORD = "qwerty"
    DB_NAME = "postgres"
    SQLALCHEMY_DATABASE_URI = ('postgresql://{}:{}@localhost/{}'.format(DB_USER, DB_USER_PASSWORD, DB_NAME))
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nhzv"
    MAX_SONG_LENGTH_IN_LINES = 50
    GROUP_PER_PAGE = 5
    SONG_PER_PAGE = 5


class TestConfig:
    DB_USER = "postgres"
    DB_USER_PASSWORD = "qwerty"
    DB_NAME = "postgres"
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = os.environ.get("SECRET_KEY") or "nhzv"
    MAX_SONG_LENGTH_IN_LINES = 50
    GROUP_PER_PAGE = 5
    SONG_PER_PAGE = 5
