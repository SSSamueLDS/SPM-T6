import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint

from datetime import datetime
import json
from os import environ

app = Flask(__name__)

CORS(app)
from Manager.manager import Manager

class HR(Manager):
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
    
    def create_role_listing():
        pass
    
    def update_role_listing():
        pass
    
    def create_skill_listing():
        pass
    
    def map_skill_to_role():
        pass
    
    def update_staff_skill():
        pass
    
    

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__))
    app.run(host='0.0.0.0', port=5002, debug=True)