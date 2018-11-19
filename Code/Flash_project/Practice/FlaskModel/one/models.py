from App.ext import db


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16))

    def save(self):
        db.session.add(self)
        db.session.commit()


class User(db.Model):

    __tablename__ = 'UserModel'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    u_name = db.Column(db.String(16), unique=True)
    u_des = db.Column(db.String(128), nullable=True)


class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    c_name = db.Column(db.String(16))


class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a_position = db.Column(db.String(16))
    a_coutomer = db.Column(db.Integer, db.ForeignKey(Customer.id))
