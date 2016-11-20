import re


signup_form = """
    <form action="" method="post">
        <label>Username: <input name="username" value="{username}"></label>{error_username}<br>
        <label>Password: <input type="password" name="password" value=""></label>{error_password}<br>
        <label>Password (confirm): <input type="password" name="verify" value=""></label>{error_verify}<br>
        <label>Email: <input name="email" value="{email}"></label>{error_email}<br><br>
        <input type="submit">
    </form>
"""


class Form(object):
    """Signup Form."""

    REQUIRED_FIELDS = ['username', 'password']
    FIELD_VALIDATION = {
        'username': r"^[a-zA-Z0-9_-]{3,20}$",
        'password': r"^.{3,20}$",
        'email': r"^[\S]+@[\S]+.[\S]+$"}

    def __init__(self, request):
        self.username = request.get('username', '')
        self.password = request.get('password', '')
        self.verify = request.get('verify', '')
        self.email = request.get('email', '')
        self.errors = {}

    def validate(self):
        self._validate_required()
        self._validate_input_content()
        self._validate_password_confirmation()
        return False if self.errors else True

    def _validate_required(self):
        for field_name in [f for f in self.REQUIRED_FIELDS if f not in self.errors]:
            if not getattr(self, field_name):
                self.errors[field_name] = 'Required'

    def _validate_input_content(self):
        for validation in [(f, v) for f, v
                           in self.FIELD_VALIDATION.iteritems() if f not in self.errors]:
            field_name, validation_string = validation
            validation_regex = re.compile(validation_string)
            field_value = getattr(self, field_name)
            if field_value and not validation_regex.match(getattr(self, field_name)):
                self.errors[field_name] = 'Invalid'

    def _validate_password_confirmation(self):
        if self.password and self.password != self.verify:
            self.errors['verify'] = "Passwords don't match"

    def render(self):
        return signup_form.format(
            username=self.username,
            email=self.email,
            error_username=self._render_error(self.errors.get('username', '')),
            error_password=self._render_error(self.errors.get('password', '')),
            error_verify=self._render_error(self.errors.get('verify', '')),
            error_email=self._render_error(self.errors.get('email', '')),
        )

    @staticmethod
    def _render_error(error):
        return '<label style="color: red;">{}</label>'.format(error) if error else ''
