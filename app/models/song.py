from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import clear_mappers

from app import Base


class Song(Base):
    __tablename__ = 'song'
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, primary_key=True)
    title = Column(String(70))
    text = Column(Text, unique=True)
    year = Column(String(4))
    youtube_link = Column(String(300), unique=True)
    group_id = Column(Integer, ForeignKey('group.id', ondelete='CASCADE'))

    def __repr__(self):
        return "{}".format(self.title)
