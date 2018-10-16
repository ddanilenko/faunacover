from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Group(Base):
    __tablename__ = 'group'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    name = Column(String(70), unique=True)
    description = Column(Text)
    official_site = Column(String(300), unique=True)
    songs = relationship('Song', backref='group', lazy='dynamic', passive_deletes='all')

    def __repr__(self):
        return "{}".format(self.name)
