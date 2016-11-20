from app import db
from app.models import Post


class PostForm(object):
    """Post Form."""

    REQUIRED_FIELDS = ['subject', 'content']

    def __init__(self, data, post=None):
        self.subject = data.get('subject', '')
        self.content = data.get('content', '')
        self.post = post
        self.errors = {}

    def validate(self):
        self._validate_required()
        return False if self.errors else True

    def _validate_required(self):
        for field_name in [f for f in self.REQUIRED_FIELDS if f not in self.errors]:
            if not getattr(self, field_name):
                self.errors[field_name] = 'Required'

    def save(self):
        if not self.post:
            post = Post(subject=self.subject, content=self.content)
        else:
            post.subject = self.subject
            post.content = self.content
        db.session.add(post)
        db.session.commit()
        return post
