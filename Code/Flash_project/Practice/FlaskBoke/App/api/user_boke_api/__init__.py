from flask_restful import Api

from App.api.user_boke_api.user_boke_api import UserBokeResource, UserAllBokeResource, BokeAllUserResource

userboke_api = Api()

userboke_api.add_resource(UserBokeResource, '/userboke/')
userboke_api.add_resource(UserAllBokeResource, '/userboke/<int:id>/')
userboke_api.add_resource(BokeAllUserResource, '/bokeuser/<int:id>/')