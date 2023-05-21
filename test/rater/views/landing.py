from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from rater.forms import RegistrationForm, LoginForm, AttemptForm
from rater.models.climber import Climber
from rater.models.route import Route
from rater.models.attempt import Attempt


landing_bp = Blueprint('landing', __name__)

@landing_bp.route('/',)
def landingPage():
    return render_template('landing/landing.html')

