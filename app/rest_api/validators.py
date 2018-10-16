from database import session
from app.models.group import Group
from app.models.song import Song
from app.models.userprofile import UserProfile


def check_if_email_exists(**kwargs):
    user = session.query(UserProfile).filter_by(email=kwargs.get('email')).first()
    return user is None or user.id == kwargs.get('user_id')


def check_song_and_group_pair(args):
    song = session.query(Song, Group).outerjoin(Group, Group.id == Song.group_id).filter(
        Song.title == args.get('title'), Group.id == args.get('group_id')).first()
    return song is None
