from flask_restful.reqparse import RequestParser

get_user_parser = RequestParser()
get_user_parser.add_argument('name', store_missing=False)
get_user_parser.add_argument('email', store_missing=False)

post_user_parser = RequestParser()
post_user_parser.add_argument('name', required=True)
post_user_parser.add_argument('email', required=True)
post_user_parser.add_argument('password', required=True,dest='password_hash')

put_user_parser = RequestParser()
put_user_parser.add_argument('name', required=False, store_missing=False)
put_user_parser.add_argument('email', required=False, store_missing=False)
put_user_parser.add_argument('password', required=False, store_missing=False,dest='password_hash')
