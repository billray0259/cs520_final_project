# Implement testing method utilizing the strategies listed in the below links:
# https://docs.python.org/3/library/unittest.html
# https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/
# https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python
# https://www.dataquest.io/blog/unit-tests-python/

import unittest
from rater.models import Climber, Gym
from bson.objectid import ObjectId
# import sys
# sys.path.insert(0, 'src/rater/models/climber.py')


import string
import random

def gen_username():
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=10))

# Method adapted from https://www.geeksforgeeks.org/python-generate-random-string-of-given-length/
def gen_email():
    return ''.join(random.choices(string.ascii_lowercase +
                             string.digits, k=7)) + "@email.com"

# Most important tests that are essential to the main functionality of the RouteRater app:
# - Check all relationships specified in the ERD diagram
# - One account per email address (Y)
# - Only strings that represent actual emails (___@___.___, Example: 1234@email.com) are accepted
# - OPTIONAL: Passwords are secure (Contain at least one special character, one capital letter, and one digit)
#   - If you decide to implement this, then MUST DISPLAY on account creation page
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

# Test 4: Once a climber adds a favorite gym, it is stored in their favorite gyms 


# Test 5: Same as test 4 but with unfavoriting gyms

# Test 6: Each user must have an email address, username, and password

# Test 7: Email addresses must be valid (If this doesn't involve internal Flask libraries)

# Test 8: When creating user profile, "password" and "confirm password" inputs must match

# Test 9: Search functionality? (Needs to be fixed as of now)

# Test 10: The model must not accept scores greater than 10

# Test 11: The model must not accept scores less than 0

# Test 12: The model must not accept non-integer values (Ex: decimal values)

# Test 13: The model correctly classifies attempts as successful or failed based on user input

# Test 14: The overall grade for a route (assert)Equals the average of all users' inputs for that route

# Test 15: Route grade is recalculated each time a new rating is given

# Test 16: When a new friend is added, it is stored in the user's profile

# # Script copied from official python unittest website - Delete Later
# class TestStringMethods(unittest.TestCase):

#     def test_upper(self):
#         self.assertEqual('foo'.upper(), 'FOO')
#         self.assertNotEqual('foo'.upper(), 'FOo')

#     def test_isupper(self):
#         self.assertTrue('FOO'.isupper())
#         self.assertFalse('Foo'.isupper())
#         # self.assertTrue('Foo'.isupper()) # Expected to fail

#     def test_split(self):
#         s = 'hello world'
#         self.assertEqual(s.split(), ['hello', 'world'])
#         # check that s.split fails when the separator is not a string
#         with self.assertRaises(TypeError):
#             s.split(2)

# # Another example - Delete later
# def add_fish_to_aquarium(fish_list):
#     if len(fish_list) > 10:
#         raise ValueError("A maximum of 10 fish can be added to the aquarium")
#     return {"tank_a": fish_list}


# class TestAddFishToAquarium(unittest.TestCase):
#     def test_add_fish_to_aquarium_success(self):
#         actual = add_fish_to_aquarium(fish_list=["shark", "tuna"])
#         expected = {"tank_a": ["shark", "tuna"]}
#         self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()