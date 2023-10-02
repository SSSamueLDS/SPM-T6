import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from sqlalchemy import ForeignKey, ForeignKeyConstraint, PrimaryKeyConstraint

from datetime import datetime
import json
from os import environ


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

CORS(app)

class Staff(db.Model):
    __tablename__ = 'Staff'

    staff_ID = db.Column(db.Integer, primary_key=True, autoincrement=True)
    staff_fname = db.Column(db.String(50), nullable=False)
    staff_lname = db.Column(db.String(50), nullable=False)
    dept = db.Column(db.String(50), nullable=False)
    country = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    access_rights = db.Column(db.Integer, ForeignKey('System_Role.SystemRole_ID'))
    staff_roleID = db.Column(db.Integer, ForeignKey('Role.Role_ID')) 
    
    #CONSTRAINT FK_Roles FOREIGN KEY (access_rights) REFERENCES System_Role(SystemRole_ID),
    #CONSTRAINT FK_Role FOREIGN KEY (staff_roleID) REFERENCES `Role`(role_ID)  whats staff_roleID?
    # __table_args__ = (
    #     ForeignKeyConstraint(['access_rights'], ['System_Role.systemrole_ID']),
    #     ForeignKeyConstraint(['staff_roleID'], )
    # )

    def json(self):
        
        dto = {
            'staff_ID': self.staff_ID,
            'staff_fname': self.staff_fname,
            'staff_lname': self.staff_lname,
            'dept': self.dept,
            'country': self.country,
            'email': self.email,
            'access_rights': self.access_rights,
            'staff_roleID': self.staff_roleID
        }
        return dto

class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'

    staff_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    skill_ID = db.Column(db.Integer, primary_key=True, nullable=False)
    proficiency = db.Column(db.Enum('Beginner','Intermediate','Advance','Expert'), nullable=True)
    __table_args__ = (
        PrimaryKeyConstraint('staff_ID', 'skill_ID'),
        ForeignKeyConstraint(['staff_ID'], ['Staff.staff_ID']),
        ForeignKeyConstraint(['skill_ID'], ['Skill.skill_ID']),
    )
    def json(self):
        dto = {
            'staff_ID': self.staff_ID,
            'skill_ID': self.skill_ID,
        }
        return dto


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("This is flask for " + os.path.basename(__file__) + "staff")
    app.run(host='0.0.0.0', port=5002, debug=True)