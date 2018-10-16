from flask_restful import fields

from app.rest_api.song.schemas import song_schema

base_group_schema = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'official_site': fields.String,
}

extended_group_schema = dict(
    songs=fields.List(fields.Nested(song_schema))
)

extended_group_schema.update(base_group_schema)
