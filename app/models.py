from app import db

from flask_bcrypt import generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.LargeBinary())
    is_active = db.Column(db.Boolean(), default=True)
    username = db.Column(db.String(120), unique=True)

    def __init__(self, first_name, last_name, email, password, is_active=True):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)
        self.is_active = is_active
