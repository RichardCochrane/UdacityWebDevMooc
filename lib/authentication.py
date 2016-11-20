import datetime
import hashlib
import random
import string

from app.models import User


def make_password_hash(password, salt=None):
    if not salt:
        salt = make_salt()

    password_hash = hashlib.sha256("{}{}".format(password, salt)).hexdigest()
    return (password_hash, salt)


def make_salt():
    return ''.join([random.choice(string.letters) for i in range(5)])


def authenticate_user(user_name, password):
    from app.models.user import User

    user = User.get_by_username(user_name)
    if make_password_hash(password, user.salt)[0] == user.password_hash:
        return user
    return None


def get_user_from_cookie(request):
    rich_session = request.cookies.get('rich_session')
    if not rich_session:
        return

    user_name, cookie_datetime, session_hash = rich_session.split(',')
    user = User.get_by_username(user_name)
    if make_password_hash(cookie_datetime, user.salt)[0] == session_hash:
        return user
    return


def authenticated_cookie_content(user_name):
    cookie_datetime = datetime.datetime.today().strftime('%d%B%Y%H%M%s')
    user = User.get_by_username(user_name)
    session_hash = make_password_hash(cookie_datetime, user.salt)

    return ','.join([user_name, cookie_datetime, session_hash[0]])
