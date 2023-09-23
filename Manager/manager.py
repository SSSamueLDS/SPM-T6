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

class Manager():
    def __init__(self, id, name, email, password):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        
        
    
    def view_skills_of_applicants():
        pass
    
    def find_suitable_candidate_for_role():
        pass
    

if __name__ == '__main__':
    print("This is flask for " + os.path.basename(__file__))
    app.run(host='0.0.0.0', port=5002, debug=True)