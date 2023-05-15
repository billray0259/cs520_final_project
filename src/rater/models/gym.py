from rater import app
from bson.objectid import ObjectId
from rater.models import Climber

db = app.config['MONGO']

class Gym:
    def __init__(self, name, address, website, owner_id, admins=None, _id=None, image_uri=None):
        self.id = _id if _id is not None else ObjectId()
        self.name = name
        self.address = address
        self.website = website
        self.owner_id = owner_id
        self.admins = admins if admins is not None else []
        self.image_uri = image_uri
    

    @staticmethod
    def from_owner_username(name, address, website, owner_username, admins=None, _id=None, image_uri=None):
        owner = Climber.find_by_username(owner_username)
        if owner is None:
            raise ValueError(f'No user found with username {owner_username}')
        return Gym(name, address, website, owner.id, admins, _id, image_uri)


    def save(self):
        # Check for unique gym name
        existing_gym = db.gyms.find_one({'name': self.name})
        if existing_gym is not None:
            raise ValueError(f'A gym with the name {self.name} already exists.')

        return db.gyms.insert_one(self.to_document())

    
    def update(self):
        # ensure gym with id exists
        existing_gym = db.gyms.find_one({'_id': self.id})
        if existing_gym is None:
            raise ValueError(f'A gym with the id {self.id} does not exist.')
        
        return db.gyms.update_one({'_id': self.id}, {'$set': self.to_document()})


    def get_owner(self):
        return Climber.find_by_id(self.owner_id)


    def to_document(self):

        return {
            '_id': self.id,
            'name': self.name,
            'address': self.address,
            'website': self.website,
            'owner': self.owner_id,
            'admins': self.admins,
            'image_uri': self.image_uri,
        }


    @staticmethod
    def from_document(doc):
        admins = doc['admins'] if 'admins' in doc else []

        return Gym(
            doc['name'],
            doc['address'] if 'address' in doc else None,
            doc['website'] if 'website' in doc else None,
            doc['owner'],
            admins,
            doc['_id'],
            doc['image_uri'] if 'image_uri' in doc else None,
        )


    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        gym_doc = db.gyms.find_one({'_id': _id})
        if gym_doc is None:
            return None
        return Gym.from_document(gym_doc)
    

    @staticmethod
    def find_by_name(name):
        gym_doc = db.gyms.find_one({'name': name})
        if gym_doc is None:
            return None
        return Gym.from_document(gym_doc)


    @staticmethod
    def find_all():
        return [Gym.from_document(doc) for doc in db.gyms.find()]

    @staticmethod
    def get_favorite_gyms(climber):
        return [Gym.from_document(gym) for gym in db.gyms.find({'_id': {'$in': climber.gyms}})]
