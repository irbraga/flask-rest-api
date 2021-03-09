from flask import Blueprint
from flask_restx import Api
from namespaces.admin.system import system_ns

admin_blueprint = Blueprint(name='admin', import_name=__name__, url_prefix='/admin')

# https://swagger.io/docs/specification/2-0/authentication/
__auth_types = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization"
    }
}

admin_api = Api(admin_blueprint, 
                title='Admin API', 
                description='Api endpoints with admin privileges.', 
                version='00.01', 
                default_mediatype='application/json',
                authorizations=__auth_types)

admin_api.add_namespace(system_ns)
