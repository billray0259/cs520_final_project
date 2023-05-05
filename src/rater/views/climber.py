from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, current_user, logout_user, login_required
from rater.forms import RegistrationForm, LoginForm
from rater.models.climber import Climber
from rater.models.route import Route
from rater.models.attempt import Attempt


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


@climber_bp.route('/logout')
def logout():
    # Log out the current user
    logout_user()

    # Redirect to the login page
    return redirect(url_for('climber.login'))

@climber_bp.route('/profile')
def profile():
    attempts = current_user.get_all_attempts()
    return render_template('climber/profile.html', current_user=current_user, attempts=attempts)

@climber_bp.route('/profile/edit')
@login_required
def edit_profile():
    return render_template('climber/edit_profile.html')

@climber_bp.route('/profile/friends')
def friends():
    name = request.args.get('name', None)

    climbers = []
    if name:
        climbers = Climber.find_many_by_username(name)

    return render_template('climber/friends.html', current_user=current_user, climbers=climbers)

@climber_bp.route('/profile/add_friend/<user_id>', methods=['GET'])
@login_required
def add_friend(user_id):
    # Retrieve the gym
    user = Climber.find_by_id(user_id)
    if not user or current_user.is_friend(user):
        return redirect(url_for('climber.friends'))

    current_user.add_friend(user)

    # Redirect back to the gym's page
    flash(f'Added {user.username} to your favorites.')
    return redirect(url_for('climber.friends', current_user=current_user, climbers=[]))

@climber_bp.route('/profile/remove_friend/<user_id>', methods=['GET'])
@login_required
def remove_friend(user_id):
    user = Climber.find_by_id(user_id)
    if not user or not current_user.is_friend(user):
        return redirect(url_for('climber.friends'))

    current_user.remove_friend(user)

    flash(f'Removed {user.username} to your favorites.')
    return redirect(url_for('climber.friends', current_user=current_user, climbers=[]))

@climber_bp.route('/route/add/<route_id>', methods=["GET"])
@login_required
def add_attempt(route_id):
    route = Route.find_by_id(route_id)
    attempt = Attempt(success=True, route_id=route.id, climber_id=current_user.id)

    # Save to database
    try:
        attempt.save()
    except ValueError as e:
        errors = [str(e)]
        return render_template('route.view', route_id=route_id, errors=errors)

    
    flash(f'Added attempt for {route.name}.')
    return redirect(url_for('route.view', route_id=route_id))