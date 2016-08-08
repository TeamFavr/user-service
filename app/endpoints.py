from flask import Blueprint

from .models import User

user = Blueprint('user', __name__)


@user.route("/")
def index():
    return 'User index'
