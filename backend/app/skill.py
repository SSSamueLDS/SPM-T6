import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Skill
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
        
    @app.route("/skills", methods=['GET'])
    def get_all_skills():
        # fetch all skills from the database
        skills = Skill.query.all()
        if skills:
            return jsonify({
                "code": 200,
                "data": [skill.json() for skill in skills]
            })
        return jsonify({
            "code": 404,
            "message": "No skills found.",
            "data": []
        })

    @app.route("/skills/<int:skill_id>", methods=['GET'])
    def get_all_name(skill_id):
        # fetch all skills from the database
        skill = Skill.query.get(skill_id)
        if skill:
            return jsonify({
                "code": 200,
                "data": {
                    "skill_id": skill_id,
                    "skill_name": skill.skill_name
                }
            })
        return jsonify({
            "code": 404,
            "message": "No skill found for id {skill_id}"
        })


    @app.route("/add_skill", methods=['POST'])
    def add_skill():
        #find if skill exists in database
        try:
            data = request.get_json()
            print(data)
            skill_name = data['skill_name']
            # capitalise first letter of every word in skill name
            skill_name = skill_name.title()
            skill = Skill.query.filter_by(skill_name=skill_name).first()
            if skill:
                return jsonify({
                    "code": 201,
                    "data": {
                        "skill_name": skill_name
                    },
                    "message": "Skill already exists."
                }), 201
            else:
                skill = Skill(skill_name=skill_name)
                db.session.add(skill)
                db.session.commit()
                return jsonify({
                    "code": 200,
                    "data": {
                    "skill_name": skill_name
                    },
                    "message": "Skill added successfully."
                }), 200
        except:
            return jsonify({
                "code": 500,
                "message": "Connection failure with the database."
            }), 500

if __name__ == '__main__':
    main()
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "skills")
    app.run(host='0.0.0.0', port=5003, debug=True)