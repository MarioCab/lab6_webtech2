from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField
from wtforms.validators import ValidationError

class LoginForm(FlaskForm):
    passcode = PasswordField("Passcode:")
    submit = SubmitField("Login")

    def validate_passcode(form, field):
        if field.data is None or len(field.data) == 0:
            raise ValidationError("Enter a passcode")

