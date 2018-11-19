from App.ext import db
from App.models import BaseModel
from App.models.boke_model import BokeModel
from App.models.user_model import BokeUserModel


class UserBokeModel(BaseModel):
    b_user_id = db.Column(db.Integer, db.ForeignKey(BokeUserModel.id))
    b_boke_id = db.Column(db.Integer, db.ForeignKey(BokeModel.id))
