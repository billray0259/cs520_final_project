from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, current_user
from rater.forms import RegistrationForm, LoginForm
from rater.models.climber import Climber

climber_bp = Blueprint('climber', __name__)

@climber_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        # Create new climber
        climber = Climber(email=form.email.data, username=form.username.data)
        climber.set_password(form.password.data)

        # Save climber to database
        try:
            climber.save()
        except ValueError as e:
            errors = [str(e)]
            return render_template('climber/register.html', form=form, current_user=current_user, errors=errors)

        # Log in new user and redirect to index page
        login_user(climber)
        return redirect(url_for('index'))

    # Render sign-up page
    return render_template('climber/register.html', form=form, current_user=current_user)


@climber_bp.route('/login', methods=['GET', 'POST'])
def login():

    # if climber is logged in redirect to index page
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()

    if form.validate_on_submit():
        # Get climber from database
        climber = Climber.find_by_email(form.email.data)

        # Check if climber exists and password is correct
        if climber is None or not climber.check_password(form.password.data):
            errors = ['Invalid email or password']
            return render_template('climber/login.html', form=form, current_user=current_user, errors=errors)

        # Log in user and redirect to index page
        login_user(climber)
        return redirect(url_for('index'))

    # Render login page
    return render_template('climber/login.html', form=form, current_user=current_user)


