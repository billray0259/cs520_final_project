from datetime import datetime
from bson.objectid import ObjectId
from rater import app
from rater.models import Climber, Route

db = app.config['MONGO']


class Attempt:
    def __init__(self, success, route_id, climber_id, time=None, _id=None):
        self.id = _id if _id is not None else ObjectId()
        self.success = success
        self.route_id = route_id
        self.climber_id = climber_id
        self.time = time if time is not None else datetime.utcnow()


    def save(self):
        # make sure an attempt with the same climber and time doesn't already exist
        if db.attempts.find_one({'climber_id': self.climber_id, 'route_id': self.route_id, 'time': self.time}):
            raise ValueError(f'Attempt already exists for climber {self.climber_id} on route {self.route_id} at time {self.time}')
        
        # add the attempt to the database
        return db.attempts.insert_one(self.to_document())
        

    def to_document(self):
        return {
            '_id': self.id,
            'success': self.success,
            'route_id': self.route_id,
            'climber_id': self.climber_id,
            'time': self.time,
        }


    @staticmethod
    def from_document(doc):
        return Attempt(
            doc['success'],
            doc['route_id'],
            doc['climber_id'],
            doc['time'],
            doc['_id'],
        )


    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        attempt_doc = db.attempts.find_one({'_id': _id})
        if attempt_doc is None:
            return None
        return Attempt.from_document(attempt_doc)


    def get_climber(self):
        return Climber.find_by_id(self.climber_id)


    def get_route(self):
        return Route.find_by_id(self.route_id)


    @staticmethod
    def find_by_climber(climber):
        attempt_docs = db.attempts.find({'climber_id': climber.id})
        return [Attempt.from_document(doc) for doc in attempt_docs]


    @staticmethod
    def find_by_route(route):
        attempt_docs = db.attempts.find({'route_id': route.id})
        return [Attempt.from_document(doc) for doc in attempt_docs]


    @staticmethod
    def find_by_climber_and_route(climber, route):
        attempt_doc = db.attempts.find_one({'climber_id': climber.id, 'route_id': route.id})
        if attempt_doc is None:
            return None
        return Attempt.from_document(attempt_doc)


    @staticmethod
    def count_successful_attempts(route):
        return db.attempts.count_documents({'route_id': route.id, 'success': True})


    @staticmethod
    def count_attempts(route):
        return db.attempts.count_documents({'route_id': route.id})
