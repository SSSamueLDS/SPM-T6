import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Staff, StaffSkill, AccessControl, Skill, RoleSkill, Role
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


    @app.route("/roles", methods=['GET'])
    def get_all_roles():
        # fetch all roles from the database
        roles = Role.query.all()
        if roles:
            return jsonify({
                "code": 200,
                "data": [role.json() for role in roles]
            })
        return jsonify({
            "code": 404,
            "message": "No roles found.",
            "data": []
        })

    # This is to find all the skills given specific role id
    @app.route("/role_skill/<int:role_id>", methods=['GET'])
    def get_skills_by_role(role_id):
        try:
            role_skills = RoleSkill.query.filter_by(role_id=role_id).all()
            skills = [role_skill.skill_id for role_skill in role_skills]
            if role_skills:
                return jsonify({
                    "code": 200,
                    "data": {
                        "role_id": role_id,
                        "skill_ids": skills
                    }
                })
            return jsonify({
                "code": 404,
                "message": "No skills found for the given role id."
            }), 404

        except Exception as e:
            app.logger.error(f"Error occurred: {e}")
            return jsonify({
                "code": 500,
                "message": "Internal Server Error"
            }), 500

    @app.route('/role_skill', methods =['GET'])
    def get_all_role_skill():
        role_skills = RoleSkill.query.all()
        role_skill_map = {}
        
        for rs in role_skills:
            if rs.role_id not in role_skill_map:
                role_skill_map[rs.role_id] = []
            role_skill_map[rs.role_id].append(rs.skill_id)
        
        return jsonify(
            {
                "code": 201,
                "data": role_skill_map
            }
        ), 201

if __name__ == '__main__':
    main()
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5005, debug=True)
