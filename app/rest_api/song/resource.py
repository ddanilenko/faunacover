import random

from flask import request
from flask_restful import Resource, marshal_with, abort
from sqlalchemy import update as upd, delete

from app import application
from app.database import session
from app.models.song import Song
from .schemas import song_schema, new_song_schema, extended_song_schema
from .parsers import get_song_parser, post_song_parser, put_song_parser
from app.authorisation import auth
from app.rest_api.validators import check_song_and_group_pair
from app.helpers import add_group_or_song


class SongResource(Resource):

    @marshal_with(extended_song_schema)
    def get(self, song_id=None, page=1, per_page=application.config.get('SONG_PER_PAGE')):
        args = get_song_parser.parse_args()
        if song_id:
            song = session.query(Song).filter_by(id=song_id).first()
            if not song:
                abort(404, message='There is no song with such id')
            return song, 200
        else:
            if args.get('page'):
                page = args.get('page')
            if args.get('per_page'):
                per_page = args.get('per_page')
            songs = session.query(Song).slice((page - 1) * per_page, page * per_page).all()
            return songs, 200

    def put(self, song_id):
        args = put_song_parser.parse_args()
        if not check_song_and_group_pair(args):
            abort(400, message='Such song from this group already exists')
        try:
            session.execute(upd(Song).where(Song.id == song_id).values(**args))
            session.commit()

        except Exception as e:
            session.rollback()
            abort(400, message='Text and youtube link should be unique')
        return 200

    @marshal_with(song_schema)
    def post(self):
        song_list = request.json[:]
        if not song_list:
            abort(400, message='Your request is empty')
        added_songs = add_group_or_song(song_list, post_song_parser, Song,
                                        validators=[{'func': check_song_and_group_pair,
                                                     'error_text': 'Such song from this group already exists'}])
        return added_songs, 201

    def delete(self, song_id):
        try:
            session.execute(delete(Song).where(Song.id == song_id))
            session.commit()
        except Exception as e:
            session.rollback()
        return 200


class CreateSongByGroupId(Resource):

    @auth.login_required
    @marshal_with(new_song_schema)
    def get(self, group_id):
        args = get_song_parser.parse_args()
        if args.get('lines') is None:
            args['lines'] = application.config.get('MAX_SONG_LENGTH_IN_LINES')
        if args.get('lines') > application.config.get('MAX_SONG_LENGTH_IN_LINES'):
            abort(400, message="The song can't have more than 50 lines. Please choose another number of lines")
        songs = session.query(Song).filter_by(group_id=group_id).all()
        if songs:
            texts = '\n'.join([song.text for song in songs])
            lines = texts.split('\n')
            while len(lines) < args.get('lines'):
                n = args.get('lines') // len(lines)
                lines = lines * (n + 1)
            new_song_text = '\n'.join(random.sample(lines, args.get('lines')))
            new_song = {
                'group': songs[0].group.name,
                'text': new_song_text
            }

            return new_song, 200
        else:
            abort(400, message='There is no such group')
