from flask_restful import fields

cut_group_schema = {
    'id': fields.Integer,
    'name': fields.String,
}

song_schema = {
    'id': fields.Integer,
    'title': fields.String,
    'text': fields.String,
    'year': fields.String,
    'youtube_link': fields.String,
}

extended_song_schema = dict(
    group=fields.Nested(cut_group_schema)
)

extended_song_schema.update(song_schema)

new_song_schema = {
    'group': fields.String,
    'text': fields.String,
}
