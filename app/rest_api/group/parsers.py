from flask_restful.reqparse import RequestParser

get_group_parser = RequestParser()
get_group_parser.add_argument('name', store_missing=False)
get_group_parser.add_argument('description', store_missing=False)
get_group_parser.add_argument('official_site', store_missing=False)
get_group_parser.add_argument('extended', type=int, store_missing=False)
get_group_parser.add_argument('page', type=int, store_missing=False)
get_group_parser.add_argument('per_page', type=int, store_missing=False)

put_group_parser = RequestParser()
put_group_parser.add_argument('name', required=False, store_missing=False)
put_group_parser.add_argument('description', required=False, store_missing=False)
put_group_parser.add_argument('official_site', required=False, store_missing=False)


def post_group_parser(group_item):
    result = {}
    for i in ('name', 'description', 'official_site'):
        if i in group_item.keys():
            result.update([(i, group_item.get(i))])
        else:
            return None
    return result


