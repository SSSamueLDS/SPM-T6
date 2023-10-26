import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Staff, StaffSkill, AccessControl, Skill

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

@app.route('/staffs/<int:userID>', methods=['GET'])
def get_staff_by_id(userID):
    staff = Staff.query.filter_by(staff_id = userID).first()
    if staff:
        return jsonify({
            "code": 200,
            "data": staff.json()
        }), 200
    return jsonify({
        "code": 404,
        "message": "No staff found for the given ID."
    }), 404

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
    
@app.route("/staffs/skills/<int:staff_id>", methods=['GET'])
def get_staff_skills(staff_id):
    
    staff_skill= StaffSkill.query.filter_by(staff_id=staff_id).all()
    if staff_skill:
        skill_list=[]
        for staff in staff_skill:
            skill_list.append(staff.skill_id)
        return jsonify({
            "code": 200,
            "data": skill_list
        })
    else:
        return jsonify({
            "code": 404,
            "message": "No skills found."
        })

@app.route("/staffs/display_skills/<int:staff_id>", methods=['GET'])
def get_staff_skills(staff_id):
    
    staff_skill= StaffSkill.query.filter_by(staff_id=staff_id).all()
    
    if staff_skill:
        skill_map={}
        skill_list=[]
        for staff in staff_skill:
            skill_list.append(staff.skill_id)
        for skill_id in skill_list:
            skill_map[skill_id]=Skill.query.filter_by(skill_id=skill_id).first().skill_name
            
        return jsonify({
            "code": 200,
            "data": skill_map
        })
    else:
        return jsonify({
            "code": 404,
            "message": "No skills found."
        })


@app.route("/access_control", methods=['GET'])
def get_all_access_control():
    access_controls = AccessControl.query.all()
    if access_controls:
        return jsonify({
            "code": 200,
            "data": [access_control.json() for access_control in access_controls]
        }), 200
    return jsonify({
        "code": 404,
        "message": "No access control found."
    }), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5004, debug=True)