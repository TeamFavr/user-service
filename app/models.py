"""Models representing tables in the database."""
from app import db

from flask_bcrypt import generate_password_hash


class User(db.Model):
    """Represents a user."""

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.LargeBinary())
    is_ad_free = db.Column(db.Boolean(), default=False)

    def __init__(self, first_name, last_name, email, password):
        """Create a User object but not save it to the database."""
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = generate_password_hash(password)

    def to_dict(self):
        """Convert instance into a dict, excluding password."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_ad_free': self.is_ad_free
        }

    def get_friends(self):
        """Return User objects for each of the instance's friends."""
        friendships = Friendship.query.filter(
            Friendship.actioning_user_id == self.id or
            Friendship.recieving_user_id == self.id,
            Friendship.confirmed == True # noqa
        )

        user_ids = set()
        for friendship in friendships:
            user_ids.add(friendship.actioning_user_id)
            user_ids.add(friendship.recieving_user_id)

        user_ids.discard(self.id)

        return User.query.filter(User.id.in_(user_ids)).all()

    def get_friend_requests(self):
        """Return all Friendship objects which the User has not accepted."""
        print("My id: {}".format(self.id))
        friend_requests = Friendship.query.filter(
            Friendship.recieving_user_id == self.id,
            Friendship.confirmed == False # noqa
        )

        return friend_requests.all()


class Friendship(db.Model):
    """Represents a relationship between two Users."""

    __table_args__ = (
        db.UniqueConstraint('actioning_user_id', 'recieving_user_id'),
        {}
    )
    id = db.Column(db.Integer, primary_key=True)
    actioning_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    recieving_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    confirmed = db.Column(db.Boolean(), default=False)

    def __init__(self, actioning_user, recieving_user, confirmed=False):
        """Create a Friendship object."""
        self.actioning_user_id = actioning_user.id
        self.recieving_user_id = recieving_user.id
        self.confirmed = confirmed

    def to_dict(self):
        """Return dictionary representing instance."""
        return {
            'id': self.id,
            'actioning_user': User.query.get(
                self.actioning_user_id).to_dict(),
            'recieving_user': User.query.get(
                self.recieving_user_id).to_dict(),
            'confirmed': self.confirmed
        }
