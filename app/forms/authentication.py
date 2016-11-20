from app import db
from app.models import User

from lib.authentication import authenticate_user, make_password_hash


class SignupForm(object):
    """Signup Form."""

    REQUIRED_FIELDS = ['username', 'password', 'password_confirm']

    def __init__(self, data, User=None):
        self.username = data.get('username', '')
        self.password = data.get('password', '')
        self.password_confirm = data.get('password_confirm', '')
        self.email = data.get('email', '')
        self.errors = {}

    def validate(self):
        self._validate_required()
        if not self.errors:
            self._validate_password_confirmation()
        return False if self.errors else True

    def _validate_required(self):
        for field_name in [f for f in self.REQUIRED_FIELDS if f not in self.errors]:
            if not getattr(self, field_name):
                self.errors[field_name] = 'Required'

    def _validate_password_confirmation(self):
        if self.password != self.password_confirm:
            self.errors['password_confirm'] = 'Passwords do not match'

    def save(self):
        password_hash, salt = make_password_hash(self.password)
        user = User(
            username=self.username, email=self.email, password_hash=password_hash, salt=salt)
        db.session.add(user)
        db.session.commit()
        return user


class LoginForm(object):
    """Login Form."""

    REQUIRED_FIELDS = ['username', 'password']

    def __init__(self, data, User=None):
        self.username = data.get('username', '')
        self.password = data.get('password', '')
        self.errors = {}

    def validate(self):
        self._validate_required()
        if not self.errors:
            self._validate_password()
        return False if self.errors else True

    def _validate_required(self):
        for field_name in [f for f in self.REQUIRED_FIELDS if f not in self.errors]:
            if not getattr(self, field_name):
                self.errors[field_name] = 'Required'

    def _validate_password(self):
        self.user = authenticate_user(self.username, self.password)
        if not self.user:
            self.errors['password'] = 'Password does not match'

    def save(self):
        return self.user
