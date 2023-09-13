import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Role(db.Model):
    __tablename__ = 'Role'
    
    role_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column(db.String(50), nullable=False)
    role_description = db.Column(db.String(255))
    deadline = db.Column(db.Date)
    
    def json(self):
        dto={
            'role_ID': self.role_ID,
            'role_name': self.role_name,
            'role_description': self.role_description,
            'deadline': self.deadline.strftime('%Y-%m-%d')
            
        }
        return dto

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

class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'

    role_ID = db.Column(db.Integer, nullable=False)
    skill_ID = db.Column(db.Integer, nullable=False)

    # db.PrimaryKeyConstraint('Role_ID', 'Skill_ID'),
    

    def json(self):
        dto = {
            'role_ID': self.role_ID,
            'skill_ID': self.skill_ID,
        }
        return dto

@app.route("/create_role", methods=['POST'])
def create_role():
    data = request.get_json()

    role_ID = data.get('role_ID')
    role_name = data.get('role_name')
    role_description = data.get('role_description')
    deadline = data.get('deadline')

    new_role = RoleSkill(role_ID=role_ID, role_name=role_name, role_description=role_description, deadline=deadline)

    try:
        db.session.add(new_role)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding new role : " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_role.json()
        }
    ), 201

@app.route("/update_role/<int:role_ID>", methods=['PUT'])
def update_role(role_ID):
    role = Role.query.filter_by(role_ID=role_ID).first()
    if role:
        data = request.get_json()
        role.role_name = data.get('role_name')
        role.role_description = data.get('role_description')
        role.deadline = data.get('deadline')
        db.session.commit()
        return jsonify(
            {
                "code": 200,
                "data": role.json()
            }
        )
    return jsonify(
        {
            "code": 404,
            "data": {
                "role_ID": role_ID
            },
            "message": "Role not found."
        }
    ), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)