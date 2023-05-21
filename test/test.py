# Implement testing method utilizing the strategies listed in the below links:
# https://docs.python.org/3/library/unittest.html
# https://machinelearningmastery.com/a-gentle-introduction-to-unit-testing-in-python/
# https://www.digitalocean.com/community/tutorials/how-to-use-unittest-to-write-a-test-case-for-a-function-in-python
# https://www.dataquest.io/blog/unit-tests-python/

import unittest

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

# class TestRouteRater(unittest.TestCase):

# Test 1: Two climbers with different usernames cannot have the same email address

# Test 2: Two climbers with different email addresses cannot have the same username

# Test 3: Two climbers with different email addresses and usernames can exist and DO NOT have the same ID

# Test 4: Once a climber adds a favorite gym, it is stored in their favorite gyms list

# Test 5: Same as test 4 but with unfavoriting gyms

# Test 6: Each user must have an email address, username, and password

# Test 7: Email addresses must be valid (If this doesn't involve internal Flask libraries)

# Test 8: When creating user profile, "password" and "confirm password" inputs must match

# Test 9: 

# Script copied from official python unittest website - Delete Later
class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        self.assertEqual('foo'.upper(), 'FOO')
        self.assertNotEqual('foo'.upper(), 'FOo')

    def test_isupper(self):
        self.assertTrue('FOO'.isupper())
        self.assertFalse('Foo'.isupper())
        # self.assertTrue('Foo'.isupper()) # Expected to fail

    def test_split(self):
        s = 'hello world'
        self.assertEqual(s.split(), ['hello', 'world'])
        # check that s.split fails when the separator is not a string
        with self.assertRaises(TypeError):
            s.split(2)

# Another example - Delete later
def add_fish_to_aquarium(fish_list):
    if len(fish_list) > 10:
        raise ValueError("A maximum of 10 fish can be added to the aquarium")
    return {"tank_a": fish_list}


class TestAddFishToAquarium(unittest.TestCase):
    def test_add_fish_to_aquarium_success(self):
        actual = add_fish_to_aquarium(fish_list=["shark", "tuna"])
        expected = {"tank_a": ["shark", "tuna"]}
        self.assertEqual(actual, expected)

if __name__ == '__main__':
    unittest.main()