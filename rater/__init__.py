print("Initializing rater package...")

import yaml
from flask import Flask
from pymongo import MongoClient
from rater.routes import (
    climber_bp,
    # route_bp,
    # gym_bp,
    # attempt_bp,
    # grade_estimate_bp,
    # comment_bp,
)

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

app = Flask(config['app_name'])
app.config['MONGO_URI'] = f'mongodb://{config["mongodb_ip_address"]}:{config["mongodb_port"]}/{config["mongodb_database"]}'
app.secret_key = config['secret_key']
mongo = MongoClient(app.config['MONGO_URI'])
app.config['MONGO'] = mongo.db

app.register_blueprint(climber_bp)
# app.register_blueprint(route_bp)
# app.register_blueprint(gym_bp)
# app.register_blueprint(attempt_bp)
# app.register_blueprint(grade_estimate_bp)
# app.register_blueprint(comment_bp)
