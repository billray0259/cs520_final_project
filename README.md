# RouteRater


## Setup

Clone the repository

`git clone https://github.com/billray0259/cs520_final_project.git`

Enter the repository directory

`cd cs520_final_project`

Create a virtual environment

`python3 -m venv .env`

Activate the environment

`source .env/bin/activate`

Install the requirements

`pip install -r requirements.txt`

Enter into the `src` directory and run `app.py`

`cd src && python app.py`


This web app is designed to improve the accuracy of difficulty ratings for indoor climbing routes. Currently, the difficulty ratings are set by the route setters and can be arbitrary, leading to inconsistent and inaccurate ratings.

The proposed solution is a web app that utilizes QR codes placed at the bottom of each route. Climbers can scan the QR code with their mobile device and be directed to a page where they can rate the route's difficulty and indicate if they were able to complete the route and how many attempts it took. The app will keep track of each climber's ratings and create a profile that reflects their climbing ability. This information will allow the app to provide a more accurate and data-driven difficulty rating for each route.

In addition to improving the accuracy of difficulty ratings, the app will enable climbers to track their skill progress over time and view their personal growth.

To use the app, simply scan the QR code at the bottom of the climbing route and rate the difficulty. Your profile will keep track of your progress and the app will update the route's difficulty rating based on the collective ratings of all climbers.

## Directions for using RouteRater

In order to create an account, click "Sign Up" on the home page and enter in your email, username, and password.



(Explain how the RouteRater app follows the MVC pattern)

./rater/views/route.py

./rater/views/grade_estimate.py

./rater/views/comment.py
./rater/views/attempt.py
./templates/gym/edit.html
./templates/climber/profile.html
./templates/climber/edit_profile.html
./templates/route/read.html
./templates/route/edit.html
./templates/route/create.html