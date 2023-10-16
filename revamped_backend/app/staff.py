import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Staff

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

CORS(app)

@app.route("/staffs", methods=['GET'])
def get_all_staffs():
    # fetch all roles from the database
    staffs = Staff.query.all()
    if staffs:
        return jsonify({
            "code": 200,
            "data": [staff.json() for staff in staffs]
        })
    return jsonify({
        "code": 404,
        "message": "No roles found."
    })

@app.route("/staffs/dept", methods=['GET'])
def get_all_depts():
    # fetch all unique departments from the staff table
    depts = db.session.query(Staff.dept).distinct().all()
    if depts:
        depts_list = [dept[0] for dept in depts]
        return jsonify({
            "code": 200,
            "data": depts_list
        })
    return jsonify({
        "code": 404,
        "message": "No departments found."
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5004, debug=True)