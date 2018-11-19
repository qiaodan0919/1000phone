import random

from flask import Blueprint, render_template, request

from App.ext import db, cache
from one.models import Student, Customer, Address

blue = Blueprint('blue', __name__, url_prefix='/one')


def init_view(app):
    app.register_blueprint(blue)


@blue.route('/')
def index():
    return render_template('base.html')


@blue.route('/addstudent/')
def add_student():
    student = Student()
    student.name = 'qiao'

    student.save()
    return "Add Success"


@blue.route('/addstudents/')
def add_students():
    students = []
    for i in range(10):
        student = Student()
        student.name = 'xiaoming%s' % i
        students.append(student)
    db.session.add_all(students)
    db.session.commit()
    return 'add stusents'


@blue.route('/getstudent/')
def get_student():
    # students = Student.query.first()
    # students = Student.query.last()
    # students = Student.query.get_or_404(20)
    # students = Student.query.get(15)
    students = Student.query.filter(Student.id.contains('xiaoming'))
    # students = Student.query.filter(Student.id > 2)
    # print(students)

    return render_template('student.html', title='student', students=students)


@blue.route('/deletestudent/')
def delete_stu():
    student = Student.query.first()

    db.session.delete(student)
    db.session.commit()

    return 'delete success'


@blue.route('/updatestudent/')
def update_stu():
    student = Student.query.first()

    student.name = 'tom'
    student.save()

    return 'update success'


@blue.route('/addcustomer/')
def add_customer():
    for i in range(5):
        customer = Customer()
        customer.c_name = '剁手党%d' % random.randrange(1000)
        db.session.add(customer)
    db.session.commit()
    return 'add success'


@blue.route('/addaddress/')
def add_address():
    address = Address()
    address.a_position = '宝盛里%d' % random.randrange(1000)
    address.a_coutomer_id = Customer.query.order_by('-id').first().id


@blue.route('/getcustomer/')
# @cache.cached(timeout=60)
def get_customer():

    # dogs = Dog.query.paginate().items
    pagination = Customer.query.paginate()

    per_page = request.args.get('per_page', 20, type=int)
    print('数据库')

    return render_template('index.html', pagination=pagination, per_page=per_page, title='customer')

