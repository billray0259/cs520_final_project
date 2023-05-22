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
from rater import app
from bson.objectid import ObjectId
from statistics import mean

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
# import sys
# sys.path.insert(0, 'src/rater/models/climber.py')

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

# # Method taken from views/route.py to be tested
# def delete(route_id):
#     try:
#         # Convert route_id to ObjectId
#         route_id = ObjectId(route_id)

#         # Fetch the route
#         route = Route.objects.get(id=route_id)

#         # Check if current user is the owner or admin of the gym
#         if current_user.id != route.gym.owner_id and current_user.id not in route.gym.admins:
#             flash('You do not have permission to delete this route.', 'danger')
#             return redirect(url_for('route.view', route_id=str(route_id)))

#         # Delete the route
#         route.delete()
#     except ValueError as e:
#         flash('Invalid route id.', 'danger')
#         return redirect(url_for('route.index'))
#     except DoesNotExist as e:
#         flash('Route does not exist.', 'danger')
#         return redirect(url_for('route.index'))

#     flash('Route deleted successfully.', 'success')
#     return redirect(url_for('gym.show', gym_id=str(route.gym.id)))

# Most important tests that are essential to the main functionality of the RouteRater app:
# - Check all relationships specified in the ERD diagram
# - One account per email address (Y)
# - Only strings that represent actual emails (___@___.___, Example: 1234@email.com) are accepted
# - All accounts and their associated values (email, password, friends, favorite gyms, route attempts, etc.) are properly stored and not forgotten
#   - Write multiple tests for all of these associated values
# - Searching gyms produces all possible results for a given search (For example, a search for "gym" brings up gyms 0-13)
# - Invalid grades for trails are not accepted
# - Something related to backend page functionality (Try to fix these)
#   - Example: Searching for gyms does not currently work
#   - Example: Profile cannot be edited
#   - Example: Dates and grades are not properly shown
#   - Should users be allowed to add gyms themselves?

class TestRouteRater(unittest.TestCase):

# # Test 1: Two climbers with different usernames cannot have the same email address
#     def test_email(self):
#         fixed_email = gen_email()
#         climber1 = Climber(fixed_email, gen_username(), ObjectId(), None, [], [])
#         climber1.set_password('password')
#         climber2 = Climber(fixed_email, gen_username(), ObjectId(), None, [], [])
#         climber2.set_password('password')

#         with self.assertRaises(ValueError):
#             climber1.save()
#             climber2.save()


# # Test 2: Two climbers with different email addresses cannot have the same username
#     def test_username(self):
#         fixed_username = gen_username()
#         climber1 = Climber(gen_email(), fixed_username, ObjectId(), None, [], [])
#         climber1.set_password('password')
#         climber2 = Climber(gen_email(), fixed_username, ObjectId(), None, [], [])
#         climber2.set_password('password')

#         with self.assertRaises(ValueError):
#             climber1.save()
#             climber2.save()

# # Test 3: Two climbers with different email addresses and usernames can exist and DO NOT have the same ID
#     def test_diffemailanduser(self):
#         climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
#         climber1.set_password('password')
#         climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
#         climber2.set_password('password')

#         # Should not return ValueError
#         climber1.save()
#         climber2.save()

#         self.assertNotEqual(climber1.id, climber2.id)

# Test 3: Two climbers with different email addresses and usernames can exist and DO NOT have the same ID
    def test_invalidemail(self):
        climber1 = Climber(gen_username(), gen_username(), ObjectId(), None, [], [])
        climber1.set_password('password')

        # Should not return ValueError
        climber1.save()

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

# Test 9: Search functionality? (Needs to be fixed as of now)


# Test 10: The model must not accept scores greater than 10
# (CHECKED IN FORMS)

# Test 11: The model must not accept scores less than 0
# (CHECKED IN FORMS)

# Test 12: The model must not accept non-integer values (Ex: decimal values)
# (CHECKED IN FORMS) - IntegerField

# Test 13: The model correctly classifies attempts as successful or failed based on user input
# (CHECKED IN FORMS) - BooleanField

# Test 14: The overall grade for a route (assert)Equals the average of all users' inputs for that route
    def test_routegrade(self):
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", "https://www.lafitness.com", ObjectId(), None, ObjectId(), None)
        gym1.save()

        grade_testlist = [7, 3, 10, 5]
        fixed_routeid = ObjectId()
        route1 = Route(gen_route_name, "Red", gym1.id, None)
        route1.save()

        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.save()
        climber2.save()

        attempt1 = Attempt(True, fixed_routeid, climber1.id, grade_testlist[0], None, None)
        attempt2 = Attempt(False, fixed_routeid, climber1.id, grade_testlist[1], None, None)
        attempt3 = Attempt(True, fixed_routeid, climber2.id, grade_testlist[2], None, None)
        attempt4 = Attempt(False, fixed_routeid, climber2.id, grade_testlist[3], None, None)
        attempt1.save()
        attempt2.save()
        attempt3.save()
        attempt4.save()

        #self.assertEqual(len(grade_testlist), route1.get_num_attempts())
        #self.assertEqual(len(grade_testlist), route1.get_num_grade_estimates())
        self.assertEqual(mean(grade_testlist), route1.get_grade_estimate())

# Test 15: Route grade is recalculated each time a new rating is given
    def test_gradechange(self):
        gym1 = Gym(gen_gym_name(), "120 East St, Hadley, MA", "https://www.lafitness.com", ObjectId(), None, ObjectId(), None)
        gym1.save()

        grade_testlist = [7, 3, 10, 5]
        fixed_routeid = ObjectId()
        route1 = Route(gen_route_name(), "Red", gym1.id, None)
        route1.save()

        climber1 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber2 = Climber(gen_email(), gen_username(), ObjectId(), None, [], [])
        climber1.save()
        climber2.save()

        attempt1 = Attempt(True, fixed_routeid, climber1.id, grade_testlist[0], None, None)
        attempt2 = Attempt(False, fixed_routeid, climber1.id, grade_testlist[1], None, None)
        attempt3 = Attempt(True, fixed_routeid, climber2.id, grade_testlist[2], None, None)
        attempt4 = Attempt(False, fixed_routeid, climber2.id, grade_testlist[3], None, None)
        attempt1.save()
        attempt2.save()
        attempt3.save()

        temp_mean = route1.get_grade_estimate()
        attempt4.save()


        #self.assertEqual(len(grade_testlist), route1.get_num_attempts())
        #self.assertEqual(len(grade_testlist), route1.get_num_grade_estimates())
        self.assertNotEqual(temp_mean, route1.get_grade_estimate())

# Test 16: When a new friend is added, it is stored in the user's profile (Is this necessary?)

# *** VIEW TESTS ***

# Test: Searching for gyms produces at least one correct result if word is present in available gyms

# Test: 



if __name__ == '__main__':
    unittest.main()