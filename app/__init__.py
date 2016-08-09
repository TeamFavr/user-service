from flask import Flask, jsonify

from flask_sqlalchemy import SQLAlchemy

from .exceptions import CustomError
from .settings import DATABASE_NAME

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@' \
        'db/{}'.format(DATABASE_NAME)

    @app.errorhandler(CustomError)
    def custom_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response

    db.init_app(app)

    from .endpoints import user as user_blueprint
    app.register_blueprint(user_blueprint)
    return app
