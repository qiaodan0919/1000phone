from App.ext import db
from models import BaseModel


class Student(BaseModel):
    s_name = db.Column(db.String(32))