"""User model"""

import os
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from errors import EnvVarError

admin_pword = os.getenv("ADMIN_PWD")

if admin_pword is None:
    raise EnvVarError("ADMIN_PWD")


class User(UserMixin):
    """Load the default version of User class provided by flask_login and add methods"""

    pwd_hash = generate_password_hash(admin_pword)
    id = "Admin"

    @classmethod
    def check_pwd(cls, pword: str):
        """Compare stored and provided password hash"""

        return check_password_hash(pwhash=cls.pwd_hash, password=pword)
