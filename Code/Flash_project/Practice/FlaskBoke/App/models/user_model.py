from werkzeug.security import generate_password_hash, check_password_hash

from App.ext import db
from App.models import BaseModel


class BokeUserModel(BaseModel):
    u_phone = db.Column(db.String(32), unique=True)
    u_email = db.Column(db.String(64), unique=True)
    _password = db.Column(db.String(256))
    is_delete = db.Column(db.Boolean, default=False)
    u_icon = db.Column(db.String(255))
    is_super = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        raise Exception("can't access")

    @password.setter
    def password(self, password_value):
        self._password = generate_password_hash(password_value)

    def check_password(self, password_value):
        return check_password_hash(self._password, password_value)

    def check_permission(self):
        return self.is_super