from flask import current_app
from flask_restful import Resource, marshal_with, abort
from sqlalchemy import update as upd

from app.models.userprofile import UserProfile
from app.rest_api.userprofile.parsers import get_user_parser, post_user_parser, put_user_parser
from app.rest_api.validators import check_if_email_exists
from .schemas import user_profile_schema


class UserProfileResource(Resource):

    @marshal_with(user_profile_schema)
    def get(self, user_id=None):
        user = None
        if user_id:
            args = get_user_parser.parse_args()
            user = current_app.session.query(UserProfile).filter_by(id=user_id).first()
            if not user:
                abort(404, message='There is no user with such id')
        else:
            abort(405, message='you need to send POST request')
        return user, 200

    @marshal_with(user_profile_schema)
    def put(self, user_id):
        args = put_user_parser.parse_args()
        if not check_if_email_exists(user_id=user_id, email=args.get('email')):
            abort(400, message='Email is already used')
            current_app.session.execute(upd(UserProfile).where(UserProfile.id == user_id).values(**args))
        user = current_app.session.query(UserProfile).filter_by(id=user_id).first()
        user.hash_password(args.get('password_hash'))
        current_app.session.commit()
        return user, 200

    @marshal_with(user_profile_schema)
    def post(self):
        args = post_user_parser.parse_args()
        if not check_if_email_exists(email=args.get('email')):
            abort(400, message='Email is already used')
        user = UserProfile(**args)
        user.hash_password(args.get('password_hash'))
        current_app.session.add(user)
        current_app.session.commit()
        return user, 201

