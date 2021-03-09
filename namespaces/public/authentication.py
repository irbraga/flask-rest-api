import datetime
from http import HTTPStatus
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import get_jti, jwt_required, get_jwt_identity
from entities.user import User
from entities.blocklist import TokenBlockList
from plugins.jwt import generate_tokens, renew_access_token

auth_ns = Namespace('Authentication', path='/auth', description='Group of functionalities related to the user authentication.')

@auth_ns.route('/login')
class LoginResource(Resource):

    login_model = auth_ns.model(name='Login', model={
        'username': fields.String(required=True, description='Username.'),
        'password': fields.String(required=True, description='Password.')
    })

    token_model = auth_ns.model(name='JWT Tokens', model={
        'access_token': fields.String(required=True, description='JWT Access Token.'),
        'refresh_token': fields.String(required=True, description='JWT Refresh Token.')
    })

    @auth_ns.expect(login_model, validate=True)
    @auth_ns.marshal_with(token_model)
    @auth_ns.response(HTTPStatus.OK.value, 'Success')
    @auth_ns.response(HTTPStatus.BAD_REQUEST.value, 'Username and/or password are incorrect.')
    def post(self):
        '''
        User login authentication.
        '''
        username = request.json['username']
        password = request.json['password']

        user = User.get_by_username(username)

        if user and user.check_password(password):
            access_token, refresh_token = generate_tokens(user)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

@auth_ns.route('/logout')
class LogoutResource(Resource):

    @auth_ns.response(HTTPStatus.OK.value, 'Success')
    @auth_ns.response(HTTPStatus.BAD_REQUEST.value, 'Missing JWT Token.')
    @jwt_required()
    def post(self):
        '''
        User system logout.
        '''
        token_block_list = TokenBlockList()
        token_block_list.jti = get_jti()
        token_block_list.save()

@auth_ns.route('/review')
class ReviewAccessTokenResource(Resource):

    access_token_model = auth_ns.model(name='Access Token', model={
        'access_token': fields.String(required=True, description='Not fresh JWT Access Token.')
    })

    @auth_ns.response(HTTPStatus.OK.value, 'Success')
    @auth_ns.response(HTTPStatus.UNAUTHORIZED.value, 'Missing JWT Refresh Token.')
    @auth_ns.marshal_with(access_token_model)
    @jwt_required(refresh=True)
    def post(self):
        '''
        Use a refresh token to create a new, not fresh, access_token.
        '''

        user = get_jwt_identity()

        return {
            'access_token': renew_access_token(user)
        }
