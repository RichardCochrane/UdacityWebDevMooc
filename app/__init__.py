from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('config')
app.debug = True
app.testing = True


@app.errorhandler(500)
def server_error(e):
    return (
        """
        An internal error occurred: <pre>{}</pre>
        See logs for full stacktrace.
        """.format(e), 500)

db = SQLAlchemy(app)

from app.views.blog import blog_pages
from app.views.authentication import authentication_pages
from app.views.misc import misc_pages

app.register_blueprint(blog_pages, url_prefix='/blog')
app.register_blueprint(authentication_pages)
app.register_blueprint(misc_pages)

db.create_all()
