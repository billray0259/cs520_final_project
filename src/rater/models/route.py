from rater import app
from bson.objectid import ObjectId
from datetime import datetime
# from rater.models import Climber, Attempt, Comment, GradeEstimate

db = app.config['MONGO']

class Route:
    def __init__(self, name, color, gym_id, _id=None):
        self.id = _id if _id is not None else ObjectId()
        self.name = name
        self.color = color
        self.gym_id = gym_id

    def save(self):
        # Check for unique route name
        existing_route = db.routes.find_one({'name': self.name})
        if existing_route is not None:
            raise ValueError(f'A route with the name {self.name} already exists.')

        return db.routes.insert_one(self.to_document())

    def to_document(self):
        return {
            '_id': self.id,
            'name': self.name,
            'color': self.color,
            'gym': self.gym_id,
        }

    @staticmethod
    def from_document(doc):
        return Route(
            doc['name'],
            doc['color'],
            doc['gym'],
            doc['_id'],
        )

    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        route_doc = db.routes.find_one({'_id': _id})
        if route_doc is None:
            return None
        return Route.from_document(route_doc)

    @staticmethod
    def find_by_name(name):
        route_doc = db.routes.find_one({'name': name})
        if route_doc is None:
            return None
        return Route.from_document(route_doc)

    @staticmethod
    def find_by_gym_id(gym_id):
        routes_doc = db.routes.find({'gym': ObjectId(gym_id)})
        if routes_doc is None:
            return []
        return [Route.from_document(doc) for doc in routes_doc]

    def get_attempts(self):
        from rater.models import Attempt
        return [Attempt.from_document(doc) for doc in db.attempts.find({'route': self.id})]

    def get_comments(self):
        from rater.models import Comment
        return [Comment.from_document(doc) for doc in db.comments.find({'route': self.id})]

    def get_grade_estimates(self):
        from rater.models import GradeEstimate
        return [GradeEstimate.from_document(doc) for doc in db.grade_estimates.find({'route': self.id})]

    def get_num_attempts(self):
        return db.attempts.find({'route': self.id}).count()

    def get_num_comments(self):
        return db.comments.find({'route': self.id}).count()

    def get_num_grade_estimates(self):
        return db.grade_estimates.find({'route': self.id}).count()

    def get_grade_estimate(self):
        attempts =  list(db.attempts.find({'route_id': self.id, 'grade': {"$exists": True}}, {"grade":1, "_id":0}))
        attempts = list(map(lambda x: x["grade"], attempts))
        
        total = 0
        for a in attempts:
            total += a
        
        if len(attempts) == 0:
            return None

        avg = total / len(attempts)

        return avg