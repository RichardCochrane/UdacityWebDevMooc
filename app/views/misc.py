from flask import Blueprint

from lib.rot13 import convert_rot13
from app.forms.misc import rot13_form, test_form
from app.forms.signup import Form

misc_pages = Blueprint('misc_pages', __name__, template_folder='templates')


@misc_pages.route('/')
def main(self):
    return test_form


@misc_pages.route('/problem1/test_form')
def test_form_view(request):
    return str(request)


@misc_pages.route('/problem1//problem2/rot13')
def rot13(request):
    if request.POST:
        return rot13_form.format('')
    return rot13_form.format(convert_rot13(request.POST['text']))


@misc_pages.route('/problem2/signup/entry')
def signup(request):
    form = Form(request)
    if request.POST and form.validate():
        request.redirect('/problem2/signup/success?username={}'.format(form.username))
    return form.render()


@misc_pages.route('/problem2/signup/success')
def signup_success(self):
    return "Welcome {}".format(self.request.get('username'))
