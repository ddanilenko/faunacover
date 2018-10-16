from flask_restful import Resource, marshal_with, abort, marshal, request
from sqlalchemy import update as upd, delete

from app import application
from app.database import session
from app.models.group import Group
from app.helpers import add_group_or_song
from .schemas import base_group_schema, extended_group_schema
from .parsers import get_group_parser, put_group_parser, post_group_parser


class GroupResource(Resource):

    def get(self, group_id=None, page=1, per_page=application.config.get('GROUP_PER_PAGE')):
        args = get_group_parser.parse_args()
        if group_id:
            group = session.query(Group).filter_by(id=group_id).first()
            if not group:
                abort(404, message='There is no group with such id')
            if args.get('extended'):
                return marshal(group, extended_group_schema), 200
            else:
                return marshal(group, base_group_schema), 200
        else:
            if args.get('page'):
                page = args.get('page')
            if args.get('per_page'):
                per_page = args.get('per_page')
            groups = session.query(Group).slice((page - 1) * per_page, page * per_page).all()
            if not groups:
                abort(404, message='Unfortunately, we have not groups yet')
            return marshal(groups, base_group_schema), 200

    def put(self, group_id):
        args = put_group_parser.parse_args()
        try:
            session.execute(upd(Group).where(Group.id == group_id).values(**args))
            session.commit()
        except Exception as e:
            session.rollback()
            abort(400, message='Group name and official site link should be unique')
        return 200

    @marshal_with(extended_group_schema)
    def post(self):
        group_list = request.json[:]
        if not group_list:
            abort(400, message='your request is empty!')
        added_groups = add_group_or_song(group_list, post_group_parser, Group)
        if not added_groups:
            abort(400, message='Nothing was added due to error in uploaded data')
        return added_groups, 201

    def delete(self, group_id):
        try:
            session.execute(delete(Group).where(Group.id == group_id))
            session.commit()
        except Exception as e:
            session.rollback()
        return 200
