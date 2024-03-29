from werkzeug.security import check_password_hash, generate_password_hash
from rater import app
from flask_login import UserMixin
from bson.objectid import ObjectId
import re

db = app.config['MONGO']

class Climber(UserMixin):
    def __init__(self, email, username, _id=None, password_hash=None, gyms=None, friends=None):
        self.id = _id if _id is not None else ObjectId()
        self.email = email
        self.username = username
        self.password_hash = password_hash
        self.gyms = gyms if gyms is not None else []
        self.friends = friends if friends is not None else []
        self.gym_id = None


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)


    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


    def select_gym(self, gym_id):
        self.gym_id = gym_id


    def save(self):
        # Check for unique email and username
        if db.climbers.find_one({'email': self.email}) is not None:
            raise ValueError('An account with this email address already exists.')
        if db.climbers.find_one({'username': self.username}) is not None:
            raise ValueError('This username is already taken.')

        # Insert document into database
        return db.climbers.insert_one({
            '_id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
        })


    def to_document(self):
        return {
            '_id': self.id,
            'email': self.email,
            'username': self.username,
            'password_hash': self.password_hash,
            'gyms': self.gyms,
            'friends': self.friends,
        }

    
    

    def is_favorite_gym(self, gym):
        return gym.id in self.gyms


    def add_favorite_gym(self, gym):
        if not self.is_favorite_gym(gym):
            self.gyms.append(gym.id)
            db.climbers.update_one({'_id': self.id}, {'$push': {'gyms': gym.id}})


    def remove_favorite_gym(self, gym):
        if self.is_favorite_gym(gym):
            self.gyms.remove(gym.id)
            db.climbers.update_one({'_id': self.id}, {'$pull': {'gyms': gym.id}})

    def get_friends(self):
        return [f for f in db.climbers.find({'_id': {'$in': self.friends}})]

    def get_friends_size(self):
        return len([f for f in db.climbers.find({'_id': {'$in': self.friends}})])

    def is_friend(self, user):
        return user.id in self.friends

    def add_friend(self, friend):
        if not self.is_friend(friend):
            self.friends.append(friend.id)
            db.climbers.update_one({'_id': self.id}, {'$push': {'friends': friend.id}})

    def remove_friend(self, friend):
        if self.is_friend(friend):
            self.friends.remove(friend.id)
            db.climbers.update_one({'_id': self.id}, {'$pull': {'friends': friend.id}})

    @staticmethod
    def from_document(doc):
        gyms = doc['gyms'] if 'gyms' in doc else []
        friends = doc['friends'] if 'friends' in doc else []
        return Climber(
            doc['email'],
            doc['username'],
            doc['_id'],
            doc['password_hash'],
            gyms,
            friends,
        )


    @staticmethod
    def find_by_email(email):
        climber_doc = db.climbers.find_one({'email': email})
        if climber_doc is None:
            return None
        return Climber.from_document(climber_doc)


    @staticmethod
    def find_by_username(username):
        climber_doc = db.climbers.find_one({'username': username})
        if climber_doc is None:
            return None
        return Climber.from_document(climber_doc)
    
    @staticmethod
    def find_many_by_username(username):
        regex = f".*{re.escape(username)}.*"  # Escape special characters in username
        climbers = db.climbers.find({'username': {'$regex': regex, '$options': 'i'}})
        return [Climber.from_document(climber) for climber in climbers]

    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        climber_doc = db.climbers.find_one({'_id': _id})
        if climber_doc is None:
            return None
        return Climber.from_document(climber_doc)


    def get_id(self):
        return str(self.id)


    @property
    def is_authenticated(self):
        return True


    @property
    def is_active(self):
        return True


    @property
    def is_anonymous(self):
        return False
