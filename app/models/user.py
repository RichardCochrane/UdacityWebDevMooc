from app import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password_hash = db.Column(db.String(100))
    salt = db.Column(db.String(256))
    email = db.Column(db.String(200), nullable=True)

    @classmethod
    def get_by_username(cls, username):
        return cls.query.filter(cls.username.ilike(username)).one()
