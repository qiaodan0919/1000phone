from flask_restful import Api

from App.api.use_api.boke_user_api import BokeUsersResource, BokeUserActionResource, BokeUserdeleteResource

user_api = Api(prefix='/boke')

user_api.add_resource(BokeUsersResource, '/user/')

user_api.add_resource(BokeUserActionResource, '/useraction/')
user_api.add_resource(BokeUserdeleteResource, '/useraction/<int:id>/')