import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from flask_cors import CORS

from datetime import datetime
from os import environ


app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Skill(db.Model):
    __tablename__ = 'Skill'

    skill_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column(db.String(50), nullable=False)

    def json(self):
        dto = {
            'skill_ID': self.skill_ID,
            'skill_name': self.skill_name,
        }
        return dto
    
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
    app.run(host='0.0.0.0', port=5002, debug=True)