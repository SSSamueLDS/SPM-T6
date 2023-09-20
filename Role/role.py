import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint
from flask_cors import CORS

from datetime import datetime
import json
from os import environ


app = Flask(__name__, template_folder='templates', static_folder='static')
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

    role_ID = db.Column(db.Integer, ForeignKey('Role.role_ID'), primary_key=True)
    skill_ID = db.Column(db.Integer, ForeignKey('Skill.skill_ID'), primary_key=True)

    __table_args__ = (
        PrimaryKeyConstraint('role_ID', 'skill_ID'),
        ForeignKeyConstraint(['role_ID'], ['Role.role_ID']),
        ForeignKeyConstraint(['skill_ID'], ['Skill.skill_ID']),
    )

    def json(self):
        dto = {
            'role_ID': self.role_ID,
            'skill_ID': self.skill_ID
        }
        return dto

@app.route("/create_role_form", methods=['GET'])
def display_role_form():
    last_role = Role.query.order_by(Role.id.desc()).first()
    print(last_role)
    next_role_id = last_role.id + 1 if last_role else 1
    return render_template('role_listing_page.html', next_role_id=next_role_id)


@app.route("/create_role", methods=['POST'])
def create_role():
    
        data = request.get_json()

        role_name = data.get('role_name')
        role_description = data.get('role_description')
        deadline = data.get('deadline')

        new_role = Role(role_name=role_name, role_description=role_description, deadline=deadline)

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
        "message": "No roles found."
    })

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

# This is to create a new skill
@app.route('/skill', methods=['POST'])
def create_skill():
    data = request.get_json()
    skill_name = data.get('skill_name')

    new_skill = Skill(skill_name = skill_name)

    try:
        db.session.add(new_skill)
        db.session.commit()
    except Exception as e:
        return jsonify(
            {
                "code": 500,
                "message": "An error occurred while adding new skill : " + str(e)
            }
        ), 500

    return jsonify(
        {
            "code": 201,
            "data": new_skill.json()
        }
    ), 201

# This is to find all the skills given specific role id
@app.route("/role_skill/<int:role_id>", methods=['GET'])
def get_skills_by_role(role_id):
    role_skills = RoleSkill.query.filter_by(role_ID=role_id).all()
    if role_skills:
        return jsonify({
            "code": 200,
            "data": [role_skill.json() for role_skill in role_skills]
        })
    return jsonify({
        "code": 404,
        "message": "No skills found for the given role ID."
    }), 404
    
@app.route("/role_skill", methods=['POST'])
def create_role_skill():
    data = request.get_json()
    print('this is the data', data)
    # plan to loop through the selected skills and for each skills selected, add new entry to the database
    role_id = data.get('role_ID')
    skill_ids = data.get('skill_IDs')
    new_entries = []

    for skill_id in skill_ids:
        new_role_skill = RoleSkill(role_ID = role_id, skill_ID = skill_id)
        try:
            db.session.add(new_role_skill)
            db.session.commit()
            print('new entry commited')
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new role skill" + str(e)
                }
            ), 500
        
        print(json.dumps(new_role_skill.json(), default=str)) # convert a JSON object to a string and print
        new_entries.append(new_role_skill.json())
        print()

    return jsonify(
        {
            "code": 201,
            "data": new_entries
        }
    ), 201

@app.route("/role_skill/<int:role_id>", methods=['PUT'])
def update_role_skill(role_id):
    data = request.get_json()
    print('this is the data', data)
    
    # Delete all existing role-skill mappings for the given role
    try:
        RoleSkill.query.filter_by(role_ID=role_id).delete()
        db.session.commit()
    except Exception as e:
        return jsonify({"code": 500, "message": f"An error occurred while deleting old role skills: {str(e)}"}), 500

    # Add new role-skill mappings
    skill_ids = data.get('skill_IDs')
    new_entries = []
    for skill_id in skill_ids:
        new_role_skill = RoleSkill(role_ID = role_id, skill_ID = skill_id)
        try:
            db.session.add(new_role_skill)
            db.session.commit()
            print('new entry commited')
        except Exception as e:
            print(e)
            return jsonify(
                {
                    "code": 500,
                    "message": "An error occurred while adding new role skill" + str(e)
                }
            ), 500
        
        print(json.dumps(new_role_skill.json(), default=str)) # convert a JSON object to a string and print
        new_entries.append(new_role_skill.json())
        print()

    return jsonify(
        {
            "code": 201,
            "data": new_entries
        }
    ), 201


@app.route('/role-listing')
def role_listing():
    return render_template('role_listing.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)
