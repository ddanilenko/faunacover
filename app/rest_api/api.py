from flask_restful import Api

from rest_api.group.resource import GroupResource
from rest_api.groupwithsong.resources import GroupWithSongResource
from rest_api.song.resource import SongResource, CreateSongByGroupId
from rest_api.userprofile.resource import UserProfileResource


def create_api(application):
    api = Api(application)

    api.add_resource(UserProfileResource, '/user', '/user/', '/user/<int:user_id>')
    api.add_resource(GroupResource, '/group', '/group/', '/group/<int:group_id>')
    api.add_resource(GroupWithSongResource, '/group/song')
    api.add_resource(SongResource, '/song', '/song/', '/song/<int:song_id>')
    api.add_resource(CreateSongByGroupId, '/create/<int:group_id>')
