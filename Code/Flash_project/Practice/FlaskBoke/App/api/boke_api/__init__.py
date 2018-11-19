from flask_restful import Api

from App.api.boke_api.boke_api import BokeResource, BokeDeleteResource

boke_api = Api()

boke_api.add_resource(BokeResource, '/boke/')
boke_api.add_resource(BokeDeleteResource, '/boke/<int:id>/')