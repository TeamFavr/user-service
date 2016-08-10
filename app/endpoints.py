from flask import Blueprint, jsonify, request

from flask_bcrypt import check_password_hash

from .exceptions import CustomError
from .models import db, User

user = Blueprint('user', __name__)


@user.route("/")
def index():
    return 'User index'


@user.route("/authenticate", methods=["POST"])
def authenticate():
    # Get JSON data from request
    json = request.get_json()

    if 'email' not in json or 'password' not in json:
        raise CustomError(400, message='Must include an email and a password')

    # Check email
    user = User.query.filter_by(email=json['email']).first()
    if user is None:
        raise CustomError(401, message='Email or password were not found.')

    # Check password
    if not check_password_hash(user.password, json['password']):
        raise CustomError(401, message='Email or password were not found.')

    return jsonify({'success': True, 'user': user.to_dict()})


@user.route("/signup", methods=["POST"])
def signup():
    # Get JSON from request
    json = request.get_json()
    if json is None:
        raise CustomError(400, message="No JSON included or "
                                       "Content-Type is not application/json")

    expected_keys = ['first_name', 'last_name', 'email', 'password']
    if not all(key in json for key in expected_keys):
        raise CustomError(400, message="Must include a first name, last name,"
                                       "email and password.")


    # Check if email is unique
    if User.query.filter_by(email=json['email']).first() is not None:
        raise CustomError(409, message='Email already in use.')

    # TODO: Add password validation

    user = User(json['first_name'], json['last_name'], json['email'],
                json['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'user': user.to_dict()})


@user.route("/users/<int:id>")
def get_user_by_id(id):
    user = User.query.get(id)
    if user is None:
        raise CustomError(404, 'User with id: {} was not found.'.format(id))

    return jsonify({'success': True, 'user': user.to_dict()})
