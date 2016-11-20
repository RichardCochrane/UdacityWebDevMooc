from flask import Blueprint, make_response, redirect, render_template, request, url_for

from app.forms.authentication import LoginForm, SignupForm
from lib.authentication import authenticated_cookie_content, get_user_from_cookie

# from lib.views.helpers import render_template
authentication_pages = Blueprint('authentication_pages', __name__, template_folder='templates')


def return_response_with_cookie(user, redirect_url):
    cookie_content = authenticated_cookie_content(user.username)
    response = make_response(redirect(redirect_url))
    response.set_cookie('rich_session', cookie_content)
    return response


@authentication_pages.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.save()
        return return_response_with_cookie(user, url_for('blog_pages.index'))

    return render_template(
        'authentication/signup.jinja2',
        form=form, user=get_user_from_cookie(request))


@authentication_pages.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = form.save()
        return return_response_with_cookie(user, url_for('blog_pages.index'))

    return render_template(
        'authentication/login.jinja2',
        form=form, user=get_user_from_cookie(request))


@authentication_pages.route('/logout')
def signout():
    response = make_response(redirect(url_for('blog_pages.index')))
    response.set_cookie('rich_session', '')
    return response
