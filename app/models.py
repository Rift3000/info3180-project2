from . import db
from werkzeug.security import generate_password_hash


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    photo = db.Column(db.String(256))
    caption = db.Column(db.String(80))
    created_on = db.Column(db.String(80))

    def __init__(self, user_id, photo, caption, created_on):
        self.user_id = user_id
        self.photo = photo
        self.caption = caption
        self.created_on = created_on


class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    post_id = db.Column(db.Integer)

    def __init__(self, user_id, post_id):
        self.user_id = user_id
        self.post_id = post_id


class Follows(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    follower_id = db.Column(db.Integer)

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    location = db.Column(db.String(80))
    joined_on = db.Column(db.String(88))
    bio = db.Column(db.String(300))
    photo = db.Column(db.String(256))
    password = db.Column(db.String(256))

    def __init__(self, username, first_name, last_name, email, location, bio, joined_on, photo, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.location = location
        self.bio = bio
        self.photo = photo
        self.joined_on = joined_on
        self.password = generate_password_hash(password, method='pbkdf2:sha256')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return unicode(self.id)  # python 2 support
        except NameError:
            return str(self.id)  # python 3 support
