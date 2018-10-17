from flask import request, current_app
from flask_restful import Resource, marshal_with, abort

from app.helpers import add_group_or_song
from app.models.group import Group
from app.models.song import Song
from app.rest_api.group.parsers import post_group_parser
from app.rest_api.group.schemas import extended_group_schema
from app.rest_api.song.parsers import post_song_parser
from app.rest_api.validators import check_song_and_group_pair


class GroupWithSongResource(Resource):

    @marshal_with(extended_group_schema)
    def post(self):
        group_list = []
        if isinstance(request.json, dict):
            group_list.append(request.json)
        if isinstance(request.json, list):
            group_list.extend(request.json)
        if not group_list:
            abort(400, message='your request is inappropriate!')
        try:
            song_list = [dict(song, group_name=group.get('name')) for group in group_list for song in group.get('songs')]
        except TypeError as e:
            song_list = []
        added_groups = []
        if group_list:
            added_groups = add_group_or_song(group_list, post_group_parser, Group)
            for song in song_list:
                group = current_app.session.query(Group).filter_by(name=song.get('group_name')).first()
                if group:
                    song['group_id'] = group.id
            add_group_or_song(song_list, post_song_parser, Song,
                              validators=[{'func': check_song_and_group_pair,
                                           'error_text': 'Such song from this group already exists'}])

        return added_groups, 201
