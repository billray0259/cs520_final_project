from datetime import datetime
from bson.objectid import ObjectId
from rater import app
from rater.models import Climber, Route

db = app.config['MONGO']

class Comment:
    def __init__(self, content, route_id, climber_id, time=None, _id=None):
        self.id = _id if _id is not None else ObjectId()
        self.content = content
        self.route_id = route_id
        self.climber_id = climber_id
        self.time = time if time is not None else datetime.utcnow()


    def save(self):
        # Check if climber and route exist
        if Climber.find_by_id(self.climber_id) is None:
            raise ValueError(f'No climber found with id {self.climber_id}')
        if Route.find_by_id(self.route_id) is None:
            raise ValueError(f'No route found with id {self.route_id}')

        return db.comments.insert_one(self.to_document())


    def to_document(self):
        return {
            '_id': self.id,
            'content': self.content,
            'route': self.route_id,
            'climber': self.climber_id,
            'time': self.time,
        }


    @staticmethod
    def from_document(doc):
        return Comment(
            doc['content'],
            doc['route'],
            doc['climber'],
            doc['time'],
            doc['_id'],
        )


    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        comment_doc = db.comments.find_one({'_id': _id})
        if comment_doc is None:
            return None
        return Comment.from_document(comment_doc)


    @staticmethod
    def find_by_climber(climber_id):
        comments = db.comments.find({'climber': climber_id})
        return [Comment.from_document(comment_doc) for comment_doc in comments]


    @staticmethod
    def find_by_route(route_id):
        comments = db.comments.find({'route': route_id})
        return [Comment.from_document(comment_doc) for comment_doc in comments]


    def get_climber(self):
        return Climber.find_by_id(self.climber_id)


    def get_route(self):
        return Route.find_by_id(self.route_id)
