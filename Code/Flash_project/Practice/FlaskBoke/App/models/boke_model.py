from App.ext import db
from App.models import BaseModel
from App.models.user_model import BokeUserModel


class BokeModel(BaseModel):
    b_user_id = db.Column(db.Integer, db.ForeignKey(BokeUserModel.id))
    b_title = db.Column(db.String(256))
    b_content = db.Column(db.String(256))
