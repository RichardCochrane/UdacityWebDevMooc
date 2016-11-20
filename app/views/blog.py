from flask import Blueprint, redirect, render_template, request, url_for

from app.models import Post
from app.forms.blog import PostForm
from lib.authentication import get_user_from_cookie

blog_pages = Blueprint('blog_pages', __name__, template_folder='templates')


@blog_pages.route('/')
def index():
    posts = Post.all()
    return render_template(
        'blog/index.jinja2',
        posts=posts, user=get_user_from_cookie(request))


@blog_pages.route('/new', methods=['GET', 'POST'])
def new():
    form = PostForm(request.form)
    if request.method == 'POST' and form.validate():
        post = form.save()
        return redirect(url_for('.show', post_id=post.id))
    return render_template(
        'blog/new.jinja2',
        post=None, form=form, user=get_user_from_cookie(request))


@blog_pages.route('/<post_id>')
def show(post_id):
    post = Post.get_by_id(post_id)
    return render_template(
        'blog/show.jinja2',
        post=post, user=get_user_from_cookie(request))
