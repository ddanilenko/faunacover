from flask_restful import abort

from app.database import session


def add_group_or_song(instance_list, parser, model, validators=[]):
    added_instance = []
    for item in instance_list:
        args = parser(item)
        if not args:
            abort(400, message='Required args are missing')
        for validator in validators:
            if not validator.get('func')(args):
                abort(400, message=validator.get('error_text'))
        try:
            instance = model(**args)
            session.add(instance)
            session.commit()
            added_instance.append(instance)
        except Exception as e:
            session.rollback()

    return added_instance
