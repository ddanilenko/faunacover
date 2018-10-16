import random

from flask import request, current_app
from flask_restful import Resource, marshal_with, abort
from sqlalchemy import update as upd, delete

from app.authorisation import auth
from app.config import Config
from app.helpers import add_group_or_song
from app.models.song import Song
from app.rest_api.validators import check_song_and_group_pair
from .parsers import get_song_parser, post_song_parser, put_song_parser
from .schemas import song_schema, new_song_schema, extended_song_schema


class SongResource(Resource):

    @marshal_with(extended_song_schema)
    def get(self, song_id=None, page=1, per_page=Config.SONG_PER_PAGE):
        args = get_song_parser.parse_args()
        if song_id:
            song = current_app.session.query(Song).filter_by(id=song_id).first()
            if not song:
                abort(404, message='There is no song with such id')
            return song, 200
        else:
            if args.get('page'):
                page = args.get('page')
            if args.get('per_page'):
                per_page = args.get('per_page')
            songs = current_app.session.query(Song).slice((page - 1) * per_page, page * per_page).all()
            return songs, 200

    def put(self, song_id):
        args = put_song_parser.parse_args()
        if not check_song_and_group_pair(args):
            abort(400, message='Such song from this group already exists')
        try:
            current_app.session.execute(upd(Song).where(Song.id == song_id).values(**args))
            current_app.session.commit()

        except Exception as e:
            current_app.session.rollback()
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
            current_app.session.execute(delete(Song).where(Song.id == song_id))
            current_app.session.commit()
        except Exception as e:
            current_app.session.rollback()
        return 200


class CreateSongByGroupId(Resource):

    @auth.login_required
    @marshal_with(new_song_schema)
    def get(self, group_id):
        args = get_song_parser.parse_args()
        if args.get('lines') is None:
            args['lines'] = Config.MAX_SONG_LENGTH_IN_LINES
        if args.get('lines') > Config.MAX_SONG_LENGTH_IN_LINES:
            abort(400, message="The song can't have more than 50 lines. Please choose another number of lines")
        songs = current_app.session.query(Song).filter_by(group_id=group_id).all()
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
