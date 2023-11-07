from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from os import environ
from dotenv import load_dotenv
import argparse

load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuring the app...
    parser = argparse.ArgumentParser(description="select env")
    parser.add_argument("-test", action="store_true", help="Enable the test env")
    parser.add_argument("-prod", action="store_true", help="Enable the prod env")
    args, unknown = parser.parse_known_args()  # Changed from parse_args()

    if args.test:
        print("test env")
        dbURL = environ.get("testdbURL")
    elif args.prod:
        print("prod env")
        dbURL = environ.get("proddbURL")
    elif args.dev:
        print("dev env")
        dbURL = environ.get("devdbURL")
    else:
        print("Defaulting to development environment")
        dbURL = environ.get("devdbURL")  # Default to dev if no argument is given
    
    app.config['SQLALCHEMY_DATABASE_URI'] = dbURL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    CORS(app)

    return app

