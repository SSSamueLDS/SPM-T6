import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import db, Skill

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
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
        "message": "No skills found."
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
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "skills")
    app.run(host='0.0.0.0', port=5003, debug=True)