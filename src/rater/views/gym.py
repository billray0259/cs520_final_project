from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from rater.forms import GymForm
from rater.models import Gym, Climber

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
        return redirect(url_for('gym.read', gym_id=str(gym.id)))

    # Render create gym page
    return render_template('gym/create.html', form=form, current_user=current_user)
