from rater import app
from bson.objectid import ObjectId
from datetime import datetime

db = app.config['MONGO']

class GradeEstimate:
    def __init__(self, grade, route_id, climber_id, _id=None, time=None):
        self.id = _id if _id is not None else ObjectId()
        self.grade = grade
        self.route_id = route_id
        self.climber_id = climber_id
        self.time = time if time is not None else datetime.utcnow()

    def save(self):
        return db.grade_estimates.insert_one(self.to_document())

    def to_document(self):
        return {
            '_id': self.id,
            'grade': self.grade,
            'route': self.route_id,
            'climber': self.climber_id,
            'time': self.time,
        }

    @staticmethod
    def from_document(doc):
        return GradeEstimate(
            doc['grade'],
            doc['route'],
            doc['climber'],
            doc['_id'],
            doc['time'],
        )

    @staticmethod
    def find_by_id(_id):
        if type(_id) is str:
            _id = ObjectId(_id)
        grade_estimate_doc = db.grade_estimates.find_one({'_id': _id})
        if grade_estimate_doc is None:
            return None
        return GradeEstimate.from_document(grade_estimate_doc)

    @staticmethod
    def find_by_route_and_climber(route_id, climber_id):
        grade_estimate_doc = db.grade_estimates.find_one({'route': route_id, 'climber': climber_id})
        if grade_estimate_doc is None:
            return None
        return GradeEstimate.from_document(grade_estimate_doc)

    @staticmethod
    def find_all_by_route(route_id):
        grade_estimate_docs = db.grade_estimates.find({'route': route_id})
        return [GradeEstimate.from_document(doc) for doc in grade_estimate_docs]

    @staticmethod
    def find_all_by_climber(climber_id):
        grade_estimate_docs = db.grade_estimates.find({'climber': climber_id})
        return [GradeEstimate.from_document(doc) for doc in grade_estimate_docs]

    def delete(self):
        db.grade_estimates.delete_one({'_id': self.id})

    def update_grade(self, new_grade):
        db.grade_estimates.update_one({'_id': self.id}, {'$set': {'grade': new_grade}})

    def update_time(self, new_time):
        db.grade_estimates.update_one({'_id': self.id}, {'$set': {'time': new_time}})
