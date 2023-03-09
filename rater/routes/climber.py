from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from rater import db
from rater.models.climber import Climber
from rater.routes.forms import RegisterForm, EditProfileForm, LoginForm

climber_bp = Blueprint('climber', __name__)

@climber_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        climber = Climber(username=form.username.data, email=form.email.data,
                          display_name=form.display_name.data)
        climber.set_password(form.password.data)
        db.session.add(climber)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('climber.login'))
    return render_template('climber/register.html', title='Register', form=form)

@climber_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('climber.profile'))
    form = LoginForm()
    if form.validate_on_submit():
        climber = Climber.query.filter_by(email=form.email.data).first()
        if climber is None or not climber.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('climber.login'))
        login_user(climber, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('climber.profile')
        return redirect(next_page)
    return render_template('climber/login.html', title='Sign In', form=form)

@climber_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('climber.login'))

@climber_bp.route('/profile')
@login_required
def profile():
    return render_template('climber/profile.html', title='Profile')

@climber_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username, current_user.email, current_user.display_name)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.display_name = form.display_name.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('climber.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.display_name.data = current_user.display_name
    return render_template('climber/edit_profile.html', title='Edit Profile', form=form)

@climber_bp.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your account has been deleted.')
    return redirect(url_for('climber.register'))
