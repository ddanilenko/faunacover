from flask import g, current_app
from flask_httpauth import HTTPBasicAuth

from app.models.userprofile import UserProfile

auth = HTTPBasicAuth()


@auth.verify_password
def verify_password(username, password):
    user = current_app.session.query(UserProfile).filter_by(name=username).first()
    if user is None or not user.verify_password(password):
        return False
    g.user = user
    return True
