from flask import Blueprint
from flask_restx import Api
from namespaces.secured.profile import profile_ns

secured_blueprint = Blueprint(name='secured', import_name=__name__, url_prefix='/secured')

# https://swagger.io/docs/specification/2-0/authentication/
__auth_types = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "X-API-Key"
    }
}

secured_api = Api(secured_blueprint, 
                title='Secured API', 
                description='Api endpoints for authenticated users.', 
                version='00.01', 
                default_mediatype='application/json',
                authorizations=__auth_types)

secured_api.add_namespace(profile_ns)
