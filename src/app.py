from flask import redirect, url_for
from flask_login import LoginManager, current_user

from rater import app
from rater.models import Climber
from rater.views import climber_bp, gym_bp


# configure the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'climber.login'

# define the user loader function
@login_manager.user_loader
def load_user(_id):
    return Climber.find_by_id(_id)


# register the blueprints
app.register_blueprint(climber_bp)
app.register_blueprint(gym_bp)


# define the index route
@app.route('/')
def index():
    if not current_user.is_authenticated:  # Check if user is not logged in
        print("User is not logged in")
        return redirect(url_for('climber.login'))  # Redirect to sign-up page
    elif current_user.gym_id is None:  # Check if user is logged in but doesn't have a selected gym
        print("User is logged in but has not selected a gym")
        return redirect(url_for('gym.search'))  # Redirect to gym page
    else:  # User is logged in and has a selected gym
        print("User is logged in and has selected a gym")
        return redirect(url_for('route.read'))  # Redirect to route page


# run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
