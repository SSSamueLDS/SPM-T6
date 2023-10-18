import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Application, Staff, Skill, Role, RoleSkill, StaffSkill, AccessControl

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.route("/applications", methods=['GET'])
def get_all_applications():
    # fetch all roles from the database
    applications = Application.query.all()
    if applications:
        return jsonify({
            "code": 200,
            "data": [application.json() for application in applications]
        })
    return jsonify({
        "code": 404,
        "message": "No roles found."
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5005, debug=True)