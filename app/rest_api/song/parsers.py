from flask_restful.reqparse import RequestParser

get_song_parser = RequestParser()
get_song_parser.add_argument('title', store_missing=False)
get_song_parser.add_argument('text', store_missing=False)
get_song_parser.add_argument('year', store_missing=False)
get_song_parser.add_argument('youtube_link', store_missing=False)
get_song_parser.add_argument('group_id', store_missing=False)
get_song_parser.add_argument('lines', type=int, store_missing=False)
get_song_parser.add_argument('page', type=int, store_missing=False)
get_song_parser.add_argument('per_page', type=int, store_missing=False)

put_song_parser = RequestParser()
put_song_parser.add_argument('title', required=False, store_missing=False)
put_song_parser.add_argument('text', required=False, store_missing=False)
put_song_parser.add_argument('year', required=False, store_missing=False)
put_song_parser.add_argument('youtube_link', required=False, store_missing=False)
put_song_parser.add_argument('group_id', required=False, store_missing=False)


def post_song_parser(song_item):
    result = {}
    for i in ('title', 'text', 'year', 'youtube_link', 'group_id'):
        if i in song_item.keys():
            result.update({i: song_item.get(i)})
        else:
            return None
    return result
