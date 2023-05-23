# Implement testing method utilizing the strategies listed in the below links:
# https://docs.python.org/3/library/unittest.html
# https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/
# https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python
# https://www.dataquest.io/blog/unit-tests-python/


from pymongo import MongoClient
from rater import app, config
test_db_name = f'{config["mongodb_database"]}_test'
app.config['MONGO_URI'] = f'mongodb://{config["mongodb_ip_address"]}:{config["mongodb_port"]}/{test_db_name}'
mongo = MongoClient(app.config['MONGO_URI'])
app.config['MONGO'] = mongo[f'{test_db_name}']

import unittest
from rater.models import Climber, Gym, Attempt, Route
from rater.controllers import route
from rater.controllers import route_bp
from bson.objectid import ObjectId
from statistics import mean

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

db = app.config['MONGO']

import string
import random

def gen_username():
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))

# Method adapted from https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
def gen_email():
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7)) + "@email.com"

def gen_gym_name():
    return "Gym " + ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=5))

def gen_route_name():
    return "Sample Route " + ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=5))

class TestRouteRater(unittest.TestCase):

# Test 1: Two climbers with different usernames cannot have the same email address
    def test_email(self):
        fixed_email = gen_email()
        climber1 = Climber(fixed_email, gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        climber2 = Climber(fixed_email, gen_username(), ObjectId(), None, [], [])
        climber2.set_password('password')

        with self.assertRaises(ValueError):
            climber1.save()
            climber2.save()


# Test 2: Two climbers with different email addresses cannot have the same username
    def test_username(self):
        fixed_username = gen_username()
        climber1 = Climber(gen_email(), fixed_username, ObjectId(), None, [], [])
        climber1.set_password('password')
        climber2 = Climber(gen_email(), fixed_username, ObjectId(), None, [], [])
        climber2.set_password('password')

        with self.assertRaises(ValueError):
            climber1.save()
            climber2.save()

# Test 3: Two climbers with different email addresses and usernames can exist and DO NOT have the same ID
    def test_diffemailanduser(self):
        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber2.set_password('password')

        # Should not return ValueError
        climber1.save()
        climber2.save()

        self.assertNotEqual(climber1.id, climber2.id)

# # Test 3: Two climbers with different email addresses and usernames can exist and DO NOT have the same ID
#     def test_invalidemail(self):
#         climber1 = Climber(gen_username(), gen_username(), ObjectId(), None, [], [])
#         climber1.set_password('password')

#         # Should not return ValueError
#         climber1.save()

# Test 4: Once a climber adds a favorite gym, it is stored in their favorite gyms (add gym method)
    def test_addgym(self):
        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", ObjectId(), None, None, None, None)
        climber1.add_favorite_gym(gym1)

        self.assertTrue(gym1.id in climber1.gyms)

        # Test for no duplicate favorite gyms
        num_gyms = len(climber1.gyms)
        climber1.add_favorite_gym(gym1)
        self.assertEqual(num_gyms, len(climber1.gyms))


# Test 5: Same as test 4 but with unfavoriting gyms (remove gym method)
    def test_removegym(self):
        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", ObjectId(), None, None, None, None)
        climber1.add_favorite_gym(gym1)
        climber1.remove_favorite_gym(gym1)
        self.assertFalse(gym1.id in climber1.gyms)

# Test 6: Same as test 4 but with adding friends
    def test_addfriend(self):
        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        climber1s_friend = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1s_friend.set_password('password')
        
        climber1.add_friend(climber1s_friend)
        self.assertTrue(climber1s_friend.id in climber1.friends)
        
        # Test for no duplicate friends
        num_friends = len(climber1.friends)
        climber1.add_friend(climber1s_friend)
        self.assertEqual(num_friends, len(climber1.friends))

# Test 7: Same as test 5 but with removing friends
    def test_removefriend(self):
        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')
        climber1s_enemy = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1s_enemy.set_password('password')
        
        climber1.add_friend(climber1s_enemy)
        climber1.remove_friend(climber1s_enemy)
        self.assertFalse(climber1s_enemy.id in climber1.friends)

# Test 8: The overall grade for a route (assert)Equals the average of all users' inputs for that route
    def test_routegrade(self):
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", "https://www.lafitness.com", ObjectId(), None, ObjectId(), None)
        gym1.save()

        grade_testlist = [7, 3, 10, 5]
        fixed_routeid = ObjectId()
        route1 = Route(gen_route_name(), "Red", gym1.id, fixed_routeid)
        route1.save()

        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.save()
        climber2.save()

        attempt1 = Attempt(True, fixed_routeid, climber1.id, grade_testlist[0], None, ObjectId())
        attempt2 = Attempt(False, fixed_routeid, climber1.id, grade_testlist[1], None, ObjectId())
        attempt3 = Attempt(True, fixed_routeid, climber2.id, grade_testlist[2], None, ObjectId())
        attempt4 = Attempt(False, fixed_routeid, climber2.id, grade_testlist[3], None, ObjectId())
        attempt1.save()
        attempt2.save()
        attempt3.save()
        attempt4.save()

        self.assertEqual(len(grade_testlist), route1.get_num_attempts())
        self.assertEqual(mean(grade_testlist), route1.get_grade_estimate())

# Test 9: Route grade is recalculated each time a new rating is given
    def test_gradechange(self):
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", "https://www.lafitness.com", ObjectId(), None, ObjectId(), None)
        gym1.save()

        grade_testlist = [7, 3, 10, 5]
        fixed_routeid = ObjectId()
        route1 = Route(gen_route_name(), "Red", gym1.id, fixed_routeid)
        route1.save()

        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.save()
        climber2.save()

        attempt1 = Attempt(False, fixed_routeid, climber1.id, grade_testlist[0], None, ObjectId())
        attempt2 = Attempt(True, fixed_routeid, climber1.id, grade_testlist[1], None, ObjectId())
        attempt3 = Attempt(False, fixed_routeid, climber2.id, grade_testlist[2], None, ObjectId())
        attempt4 = Attempt(True, fixed_routeid, climber2.id, grade_testlist[3], None, ObjectId())
        attempt1.save()
        attempt2.save()
        attempt3.save()

        temp_mean = route1.get_grade_estimate()
        attempt4.save()

        self.assertNotEqual(temp_mean, route1.get_grade_estimate())

    # Test 10: Gym.find_all() contains the name of a gym that has been added to the database
    def test_gymsstored(self):
        gym1_name = gen_gym_name()
        gym1 = Gym(gym1_name, "113 Route 9, Hadley, MA", "https://www.24hourfitness.com/", ObjectId(), None, ObjectId(), None)
        gym1.save()

        all_gyms = Gym.find_all()
        all_gym_names = []
        all_gym_addresses = []
        all_gym_websites = []
        for gym in all_gyms:
            all_gym_names.append(gym.name)
            all_gym_addresses.append(gym.address)
            all_gym_websites.append(gym.website)

        self.assertTrue(gym1.name in all_gym_names)
        self.assertTrue("113 Route 9, Hadley, MA" in all_gym_addresses)
        self.assertTrue("https://www.24hourfitness.com/" in all_gym_websites)
    
    # Test 11: User can add and store friends


    # Test 12: Gym Owners

if __name__ == '__main__':
    unittest.main()