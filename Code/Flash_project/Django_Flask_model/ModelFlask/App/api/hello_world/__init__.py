from flask_restful import Api

from App.api.hello_world.hello_api import HelloResource

hello_api = Api(prefix='/api')

hello_api.add_resource(HelloResource, '/hello/')