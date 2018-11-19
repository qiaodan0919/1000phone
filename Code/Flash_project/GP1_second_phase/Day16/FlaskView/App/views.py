from flask import Blueprint, redirect, url_for, request

blue = Blueprint('blue', __name__)


def init_view(app):
    app.register_blueprint(blue)


@blue.route('/', methods=['GET', 'POST', 'DELETE'])
def index():
    return 'Index'


@blue.route('/users/<int:id>/')
def users(id):

    print(id)

    print(type(id))

    return 'Users API'


@blue.route('/getinfo/<string:token>/')
@blue.route('/gettoken/<int:token>/')
def get_info(token):

    print(token)

    print(type(token))

    return 'Get Success'


@blue.route('/getpath/<path:address>/')
def get_path(address):

    print(address)

    print(type(address))

    return 'Address Success'


@blue.route('/getuuid/<uuid:uu>/')
def get_uuid(uu):

    print(uu)

    print(type(uu))

    return 'UUID Success'


@blue.route('/getany/<any(a, b):an>/')
def get_any(an):

    print(an)

    print(type(an))

    return 'Any succes'


@blue.route('/redirect/')
def red():
    # return redirect('/')
    return redirect(url_for('blue.get_any', an='a'))


@blue.route('/getrequest/', methods=["GET", "POST", "PUT", "DELETE"])
def get_request():

    print(request.host)

    print(request.url)

    if request.method == "GET":
        return "GET Success %s" % request.remote_addr
    elif request.method.lower() == "post":
        return "POST Success"
    else:
        return '%s Not Support' % request.method

