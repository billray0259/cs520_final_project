from werkzeug.security import check_password_hash, generate_password_hash
from rater import app
from flask_login import UserMixin
from bson.objectid import ObjectId


db = app.config['MONGO']

class Climber(UserMixin):
    def __init__(self, email, username, id_=None, password_hash=None, gyms=None, friends=None):
        self.id = id_ if id_ is not None else ObjectId()
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
    def find_by_id(id_):
        if type(id_) is str:
            id_ = ObjectId(id_)
        climber_doc = db.climbers.find_one({'_id': id_})
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
