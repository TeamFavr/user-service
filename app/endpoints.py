"""Contains the routes for the user Blueprint."""
from flask import Blueprint, jsonify, request, g

from flask_bcrypt import check_password_hash

from .exceptions import CustomError
from .models import db, User

user = Blueprint('user', __name__)

def before_request():
    id = request.headers.get("User-Id", None)
    if id:
        user = User.query.get(id)
        if user is None:
            raise CustomError(400, message="Invalid User-Id in Header.")
        g.user = user
    else:
        g.user = None

user.before_request(before_request)


@user.route("/")
def index():
    """Index route."""
    print(request.headers)
    return 'User index'


@user.route("/authenticate", methods=["POST"])
def authenticate():
    """Return whether or not an email or password combination is valid."""
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
    """Create new User from supplied infomation."""
    # Get JSON from request
    json = request.get_json()
    if json is None:
        raise CustomError(400, message="No JSON included or "
                                       "Content-Type is not application/json")

    expected_keys = ['first_name', 'last_name', 'email', 'password']
    if not all(key in json for key in expected_keys):
        raise CustomError(400, message="Must include a first name, last name,"
                                       "email and password.")

    # # Check if email is unique
    if User.query.filter_by(email=json['email']).first() is not None:
        raise CustomError(409, message='Email already in use.')

    # # TODO: Add password validation

    user = User(json['first_name'], json['last_name'], json['email'],
                json['password'])
    db.session.add(user)
    db.session.commit()

    return jsonify({'success': True, 'user': user.to_dict()})


@user.route("/users/<int:id>")
def get_user_by_id(id):
    """Get a user by its id."""
    user = User.query.get(id)
    if user is None:
        raise CustomError(404, 'User with id: {} was not found.'.format(id))

    return jsonify({'success': True, 'user': user.to_dict()})


@user.route("/friends")
def friends():
    """Return all of the current user's friends."""
    friends = [u.to_dict() for u in g.user.get_friends()]
    return jsonify({'success': True, 'friends': friends})


@user.route("/friend-requests")
def friend_requests():
    """Return all friendships which are not confirmed for the current user."""
    pass


@user.route("/friend-request", methods=["POST"])
def create_friend_request():
    """Create an unconfirmed friendship between two users."""
    pass


@user.route("/friend-request/<int:id>", methods=["GET", "PATCH", "DELETE"])
def get_friend_request_with_id():
    """Get, update or delete friendship with the specified id."""
    pass
