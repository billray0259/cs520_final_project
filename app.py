from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_pymongo import PyMongo
from datetime import datetime

app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:27017/climbing_app'
app.secret_key = 'secret_key'
mongo = PyMongo(app)

# TODO: add authentication functionality


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = mongo.db.users.find_one({'email': email})

        if user and user['password'] == password:
            session['user_id'] = str(user['_id'])
            flash('You have been logged in.')
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')

    return render_template('login.html')



@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        birthdate = datetime.strptime(request.form['birthdate'], '%Y-%m-%d')
        terms = request.form.get('terms')

        # Check if email already exists
        user = mongo.db.users.find_one({'email': email})
        if user:
            flash('An account with this email address already exists.')
            return redirect(url_for('register'))

        # Check if passwords match
        if password != confirm_password:
            flash('Passwords do not match.')
            return redirect(url_for('register'))

        # Create new user
        new_user = {
            'email': email,
            'password': password,
            'first_name': first_name,
            'last_name': last_name,
            'birthdate': birthdate,
            'created_at': datetime.now()
        }
        mongo.db.users.insert_one(new_user)

        flash('Account created successfully. Please log in.')
        return redirect(url_for('login'))

    return render_template('register.html')



@app.route('/route/<route_id>', methods=['GET', 'POST'])
def route(route_id):
    route = mongo.db.routes.find_one_or_404({'_id': route_id})
    if request.method == 'POST':
        # TODO record rating
        flash('Your rating has been added.')
        return redirect(url_for('route', route_id=route_id))
    ratings = mongo.db.ratings.find({'route_id': route_id})
    return render_template('route.html', route=route, ratings=ratings)


@app.route('/connect', methods=['GET', 'POST'])
def connect():
    # TODO: create social connectivity functionality
    return render_template('connect.html')


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))
    user = mongo.db.users.find_one({'_id': user_id})
    ratings = mongo.db.ratings.find({'user_id': user_id})
    return render_template('profile.html', user=user, ratings=ratings)


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


@app.route('/terms')
def terms():
    return render_template('terms.html')


if __name__ == '__main__':
    app.run(debug=True)
