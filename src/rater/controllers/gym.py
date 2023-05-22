from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from rater.forms import GymForm
from rater.models import Gym, Route, Climber

gym_bp = Blueprint('gym', __name__)


@gym_bp.route('/gym/create', methods=['GET', 'POST'])
@login_required
def create():
    form = GymForm()

    if form.validate_on_submit():

        try:
            # Create new gym
            gym = Gym.from_owner_username(name=form.name.data, address=form.address.data, website=form.website.data, owner_username=form.owner_username.data)
            # Save gym to database
            gym.save()
        except ValueError as e:
            errors = [str(e)]
            return render_template('gym/create.html', form=form, current_user=current_user, errors=errors)

        # Redirect to gym page
        return redirect(url_for('gym.search', gym_id=str(gym.id)))

    # Render create gym page
    return render_template('gym/create.html', form=form, current_user=current_user)


@gym_bp.route('/gym/search', methods=['GET'])
@login_required
def search():
    # Parse query parameters
    name = request.args.get('name', None)
    gym_id = request.args.get('gym_id', None)

    # Find gyms by name or by ID
    if name:
        gyms = Gym.find_all()
        gyms = [
            gym
            for gym in gyms
            if name.lower() in gym.name.lower()
        ]
    elif gym_id:
        gym = Gym.find_by_id(gym_id)
        if gym is not None:
            return render_template('gym/search.html', gyms=[gym], current_user=current_user)
        else:
            flash('Gym not found!')
            return redirect(url_for('gym.create'))
    else:
        gyms = Gym.find_all()

    favorite_gyms = Gym.get_favorite_gyms(current_user)
    favorite_ids = set([gym.id for gym in favorite_gyms])

    gyms = [
        gym
        for gym in gyms
        if gym.id not in favorite_ids
    ]

    return render_template('gym/search.html', gyms=gyms, current_user=current_user, favorite_gyms=favorite_gyms)


@gym_bp.route('/gym/remove_favorite/<gym_id>', methods=['GET'])
@login_required
def remove_favorite(gym_id):
    # Retrieve the gym
    gym = Gym.find_by_id(gym_id)
    if not gym:
        return redirect(url_for('gym.search'))

    # Remove the gym from the current user's favorites
    current_user.remove_favorite_gym(gym)

    # Redirect back to the gym's page
    flash(f'Removed {gym.name} from your favorites.')
    return redirect(url_for('gym.search'))

# gym.add_favorite route
@gym_bp.route('/gym/add_favorite/<gym_id>', methods=['GET'])
@login_required
def add_favorite(gym_id):
    # Retrieve the gym
    gym = Gym.find_by_id(gym_id)
    if not gym:
        return redirect(url_for('gym.search'))

    # Add the gym to the current user's favorites
    current_user.add_favorite_gym(gym)

    # Redirect back to the gym's page
    flash(f'Added {gym.name} to your favorites.')
    return redirect(url_for('gym.search'))


# gym.edit route
@gym_bp.route('/gym/edit/<gym_id>', methods=['GET', 'POST'])
@login_required
def edit(gym_id):
    # Retrieve the gym
    gym = Gym.find_by_id(gym_id)
    owner = gym.get_owner()
    if not gym:
        return redirect(url_for('gym.search'))

    # Check if the current user is an admin of the gym
    if not owner.id == current_user.id:
        flash('You are not authorized to edit this gym.')
        return redirect(url_for('gym.show', gym_id=gym.id))

    # Create the form
    form = GymForm(obj=gym)
    form.owner_username.data = owner.username

    if form.validate_on_submit():
        owner_username = form.owner_username.data
        owner = Climber.find_by_username(owner_username)

        if owner is None:
            flash('Owner not found!')
            return render_template('gym/edit.html', form=form, gym=gym, current_user=current_user)

        # Update the gym
        gym.name = form.name.data
        gym.address = form.address.data
        gym.website = form.website.data
        gym.owner_id = owner.id
        gym.image_uri = form.image_uri.data

        # Update the gym to in the database
        gym.update()

        # Redirect to the gym's page
        flash('Gym updated successfully.')
        return redirect(url_for('gym.search'))

    # Render the edit page
    return render_template('gym/edit.html', form=form, gym=gym, current_user=current_user)


# gym.show route
@gym_bp.route('/gym-page/<gym_id>', methods=['GET'])
def show(gym_id):
    # Retrieve the gym
    gym = Gym.find_by_id(gym_id)
    if not gym:
        return redirect(url_for('gym.search'))

    # Retrieve the routes for the gym
    routes = Route.find_by_gym_id(gym_id)

    # Render the gym's page
    return render_template('gym/read.html', gym=gym, routes=routes, current_user=current_user)
