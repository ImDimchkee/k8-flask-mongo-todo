from flask import Flask
from flask_pymongo import PyMongo

from dotenv import find_dotenv, load_dotenv
import os

load_dotenv("flaskr/.env")

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://%s:%s@mongodb:27017/todo?authSource=admin" % (os.environ.get("MONGO_USER"), os.environ.get("MONGO_PASSWORD"))
app.config["SECRET_KEY"] = "ab8fca021a9a1296cf2073aea7bc4de7b67b59d2"

mongo_client = PyMongo(app=app)
db = mongo_client.db

from flaskr import routes
