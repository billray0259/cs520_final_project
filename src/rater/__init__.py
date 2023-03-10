import yaml
from flask import Flask
from pymongo import MongoClient

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)


app = Flask(config['app_name'])
app.config['MONGO_URI'] = f'mongodb://{config["mongodb_ip_address"]}:{config["mongodb_port"]}/{config["mongodb_database"]}'
app.secret_key = config['secret_key']
mongo = MongoClient(app.config['MONGO_URI'])
app.config['MONGO'] = mongo.db

