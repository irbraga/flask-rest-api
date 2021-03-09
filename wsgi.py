from flask import Flask, Blueprint
from flask_migrate import Migrate
from plugins.jwt import jwt_manager
from plugins.sqlalchemy import db
from werkzeug.exceptions import BadRequest, Unauthorized, InternalServerError
from cli import db_cli
from blueprints.admin import admin_blueprint
from blueprints.public import public_blueprint
from blueprints.secured import secured_blueprint
from config import ServerConfig


def create_app(config):
    # https://flask.palletsprojects.com/en/1.1.x/patterns/appfactories/

    app = Flask(__name__)
    app.config.from_object(ServerConfig)
    
    # Registering the Blueprints
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(public_blueprint)
    app.register_blueprint(secured_blueprint)

    # Initialising the Flask-SQLAlquemy
    db.init_app(app)

    # Initialising the Flask-Migrate
    Migrate(app, db)
    
    # Initialising the Flask-Jwt-Extended
    jwt_manager.init_app(app)

    # Adding command line to initialize the database with some data
    app.cli.add_command(db_cli)

    @app.errorhandler(BadRequest)
    @app.errorhandler(Unauthorized)
    @app.errorhandler(InternalServerError)
    def handle_bad_request(error):
        '''
        Handling errors.
        '''
        return {
            'message': error.message
        }, error.code
    
    @app.teardown_request
    def teardown_request(exception):
        '''
        At the end of a request, check if any exception occured. If it's True, rollback the session database transaction.
        Otherwise, commit.
        '''
        if exception:
            db.session.rollback()
        else:
            db.session.commit()

    return app
