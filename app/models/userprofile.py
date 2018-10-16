from sqlalchemy import Column, Integer, String
from passlib.apps import custom_app_context as pwd_context

from app.database import Base


class UserProfile(Base):
    __tablename__ = 'userprofile'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    email = Column(String(60), unique=True)
    password_hash = Column(String(300))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def __repr__(self):
        return "{}".format(self.name)
