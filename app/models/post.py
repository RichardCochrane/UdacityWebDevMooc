from app import db


class Post(db.Model):
    """Record of a single post in the blog."""

    __tablename__ = 'post'

    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(50))
    subject = db.Column(db.String(100))
    content = db.Column(db.Text)
    created_at = db.Column(db.DateTime)

    @classmethod
    def all(cls):
        return cls.query.all()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter(cls.id == id).one()
