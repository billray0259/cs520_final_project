import io
import base64
import qrcode

from bson import ObjectId
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required
from rater.forms import RouteForm
from rater.models import Gym, Route, Attempt

route_bp = Blueprint('route', __name__)


@route_bp.route('/route/create', methods=['GET', 'POST'])
@login_required
def create():
    form = RouteForm()

    if form.validate_on_submit():

        try:
            # convert gym_id to ObjectId
            gym_id = ObjectId(form.gym_id.data)

            # Create new route
            route = Route(form.name.data, form.color.data, gym_id)
            # Save route to database
            route.save()
        except ValueError as e:
            errors = [str(e)]
            return render_template('route/create.html', form=form, current_user=current_user, errors=errors)

        # Redirect to route page
        return redirect(url_for('route.view', route_id=str(route.id)))

    # Render create gym page
    return render_template('route/create.html', form=form, current_user=current_user)


@route_bp.route('/route/<route_id>')
@login_required
def view(route_id):
    route = Route.find_by_id(route_id)
    if route is None:
        return redirect(url_for('main.index'))

    climber_attempts = Attempt.find_by_route(route)
    estimate = route.get_grade_estimate()

    # Generate the QR code
    qrcode_img = qrcode.make(url_for('route.view', route_id=route_id, _external=True))

    # Save it to a BytesIO object
    buf = io.BytesIO()
    qrcode_img.save(buf)

    # Encode the image in base64 and convert it to a format that can be used in HTML
    qr_code_b64 = base64.b64encode(buf.getvalue()).decode()

    gym = Gym.find_by_id(route.gym_id)

    return render_template('route/read.html', route=route, current_user=current_user, climber_attempts=climber_attempts, estimate=estimate, qr_code_b64=qr_code_b64, gym=gym)

