import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Staff, StaffSkill, AccessControl, Skill
import argparse
from datetime import datetime
import json
from os import environ
from dotenv import load_dotenv

app = Flask(__name__)

load_dotenv()

def main():
    parser = argparse.ArgumentParser(description="select env")
    parser.add_argument("-test", action="store_true", help="Enable the test env")
    parser.add_argument("-prod", action="store_true", help="Enable the prod env")
    args = parser.parse_args()

    
    if args.test:
        print("test env")
        dbURL = os.getenv("testdbURL")
        
        
    elif args.prod:
        
        print("prod env")
        dbURL = os.getenv("proddbURL")
        
    else:
        print("Please Specify the environment.")
    
    app.config['SQLALCHEMY_DATABASE_URI'] = dbURL
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
        depts_list = []
        if depts:
            depts_list = [dept[0] for dept in depts]
            return jsonify({
                "code": 200,
                "data": depts_list
            })
        return jsonify({
            "code": 404,
            "message": "No departments found.",
            "data": depts_list
        })
        
    @app.route("/staffs/skills/<int:staff_id>", methods=['GET'])
    def get_staff_skills(staff_id):
        
        staff_skill= StaffSkill.query.filter_by(staff_id=staff_id).all()
        skill_list=[]
        if staff_skill:
            for staff in staff_skill:
                skill_list.append(staff.skill_id)
            return jsonify({
                "code": 200,
                "data": skill_list
            })
        else:
            return jsonify({
                "code": 404,
                "message": "No skills found.",
                "data": skill_list
            })

    @app.route("/staffs/display_skills/<int:staff_id>", methods=['GET'])
    def get_staff_skilldisplay(staff_id):
        
        staff_skill= StaffSkill.query.filter_by(staff_id=staff_id).all()
        skill_map={}
        if staff_skill:
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
                "message": "No skills found.",
                "data": skill_map
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
    main()
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5004, debug=True)