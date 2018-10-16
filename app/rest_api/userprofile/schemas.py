from flask_restful import fields

user_profile_schema = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String
}
