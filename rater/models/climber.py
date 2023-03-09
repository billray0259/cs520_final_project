from datetime import datetime
from bson.objectid import ObjectId
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from rater.models.gym import Gym

class Climber:
    collection = current_app.config['MONGO'].climbers

    def __init__(self, display_name, email, username, password):
        self.display_name = display_name
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)
        self.gyms = []
        self.friends = []
        self.id = None

    def save(self):
        document = self.__dict__
        document.pop('id', None)
        result = self.collection.insert_one(document)
        self.id = result.inserted_id

    @classmethod
    def get(cls, climber_id):
        document = cls.collection.find_one({'_id': ObjectId(climber_id)})
        return cls(**document) if document else None

    def update(self):
        document = self.__dict__
        document.pop('id', None)
        self.collection.replace_one({'_id': self.id}, document)

    def delete(self):
        self.collection.delete_one({'_id': self.id})

    @classmethod
    def find_by_username(cls, username):
        document = cls.collection.find_one({'username': username})
        return cls(**document) if document else None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def add_gym(self, gym_id):
        if not isinstance(gym_id, ObjectId):
            gym_id = ObjectId(gym_id)

        gym = Gym.get(gym_id)
        if gym and gym not in self.gyms:
            self.gyms.append(gym)
            self.update()

    def remove_gym(self, gym_id):
        if not isinstance(gym_id, ObjectId):
            gym_id = ObjectId(gym_id)
            
        gym = Gym.get(gym_id)
        if gym and gym in self.gyms:
            self.gyms.remove(gym)
            self.update()

    def add_friend(self, friend_id):
        if not isinstance(friend_id, ObjectId):
            friend_id = ObjectId(friend_id)
        friend = Climber.get(friend_id)
        if friend and friend not in self.friends:
            self.friends.append(friend)
            self.update()

    def remove_friend(self, friend_id):
        if not isinstance(friend_id, ObjectId):
            friend_id = ObjectId(friend_id)
        friend = Climber.get(friend_id)
        if friend and friend in self.friends:
            self.friends.remove(friend)
            self.update()

    def get_attempts(self):
        from rater.models.attempt import Attempt
        return [Attempt(**document) for document in Attempt.collection.find({'climber_id': self.id})]

    def get_grade_estimates(self):
        from rater.models.grade_estimate import GradeEstimate
        return [GradeEstimate(**document) for document in GradeEstimate.collection.find({'climber_id': self.id})]

    def get_comments(self):
        from rater.models.comment import Comment
        return [Comment(**document) for document in Comment.collection.find({'climber_id': self.id})]

    def to_dict(self):
        return {
            'id': str(self.id),
            'display_name': self.display_name,
            'email': self.email,
            'username': self.username,
            'gyms': [str(gym.id) for gym in self.gyms],
            'friends': [str(friend.id) for friend in self.friends],
        }


'''
Explanation:

The Climber class represents a climber in the application.
The collection attribute refers to the climbers collection in the MongoDB database.
The __init__ method initializes a new Climber object with the provided display_name, email, username, and password. The password is hashed using the generate_password_hash function from werkzeug.security.
The save method saves the Climber object to the database. It inserts a new document into the climbers collection and sets the id attribute of the Climber object to the _id value of the inserted document.
The get method retrieves a Climber object from the database by its climber_id. It queries the climbers collection for a document with the _id field matching the climber_id converted to an ObjectId, and returns a new Climber object initialized with the values from the retrieved document.
The update method updates the Climber object in the database. It replaces the document in the climbers collection with the _id field matching the id attribute of the Climber object with the updated values from the Climber object.
The delete method deletes the Climber object from the database. It removes the document from the climbers collection with the _id field matching the id attribute of the Climber object.
The find_by_username method retrieves a Climber object from the database by its username. It queries the climbers collection for a document with the username field matching the provided username, and returns a new Climber object initialized with the values from the retrieved document.
The set_password method sets a new password for the Climber object. It hashes the new password using the generate_password_hash function from werkzeug.security.
The check_password method checks if a provided password matches the Climber object's password hash. It uses the check_password_hash function from werkzeug.security.
The add_gym method adds a Gym object to the Climber object's gyms list. It retrieves the Gym object from the database using the provided gym_id, adds it to the gyms list if it exists and is not already in the list, and updates the Climber object in the database.
The remove_gym method removes a Gym object from the Climber object's gyms list. It retrieves the Gym object from the database using the provided gym_id, removes it from the gyms list if it exists and is in the list, and updates the Climber object in the database.
The add_friend method adds a Climber object to the Climber object's friends list. It retrieves the Climber object from the database using the provided friend_id, adds it to the friends list if it exists and is not
'''