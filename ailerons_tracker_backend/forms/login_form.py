"""Login form"""

from flask_wtf import FlaskForm
from wtforms import PasswordField, validators


class LoginForm(FlaskForm):
    """Login form
    Attributes:
        password: password field, required."""

    password = PasswordField("Mot de passe:", [validators.data_required()])
