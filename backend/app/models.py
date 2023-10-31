from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class AccessControl(db.Model):
    __tablename__ = 'Access_Control'

    access_id = db.Column('Access_ID', db.Integer, primary_key=True, autoincrement=True)
    access_control_name = db.Column('Access_Control_Name', db.String(50), nullable=False, unique=True)

    def json(self):
        dto = {
            'access_id': self.access_id,
            'access_control_name': self.access_control_name,
        }
        return dto

class Staff(db.Model):
    __tablename__ = 'Staff'

    staff_id = db.Column('Staff_ID', db.Integer, primary_key=True)
    staff_fname = db.Column('Staff_FName', db.String(50), nullable=False)
    staff_lname = db.Column('Staff_LName', db.String(50), nullable=False)
    dept = db.Column('Dept', db.String(50), nullable=False)
    country = db.Column('Country', db.String(50), nullable=False)
    email = db.Column('Email', db.String(50), nullable=False)
    role = db.Column('Role', db.Integer, ForeignKey('Access_Control.Access_ID'))

    def json(self):
        
        dto = {
            'staff_id': self.staff_id,
            'staff_fname': self.staff_fname,
            'staff_lname': self.staff_lname,
            'dept': self.dept,
            'country': self.country,
            'email': self.email,
            'role': self.role
        }
        return dto

class Skill(db.Model):
    __tablename__ = 'Skill'

    skill_id = db.Column('Skill_ID', db.Integer, primary_key=True, autoincrement=True)
    skill_name = db.Column('Skill_Name', db.String(250), nullable=False)
    skill_desc = db.Column('Skill_Desc', db.Text, nullable=False)

    def json(self):
        dto = {
            'skill_id': self.skill_id,
            'skill_name': self.skill_name,
            'skill_desc': self.skill_desc,
        }
        return dto

class Role(db.Model):
    __tablename__ = 'Role'
    
    role_id = db.Column('Role_ID', db.Integer, primary_key=True, autoincrement=True)
    role_name = db.Column('Role_Name', db.String(250))
    role_description = db.Column('Role_Desc', db.Text)
    
    def json(self):
        dto={
            'role_id': self.role_id,
            'role_name': self.role_name,
            'role_description': self.role_description,
        }
        return dto

class Listing(db.Model):
    __tablename__ = 'Listing'
    
    listing_id = db.Column('Listing_ID', db.Integer, primary_key=True, autoincrement=True)
    listing_name = db.Column('Listing_Name', db.String(250))
    listing_description = db.Column('Listing_Desc', db.Text)
    dept = db.Column('Dept', db.String(50))
    deadline = db.Column('Deadline', db.Date)
    hr_id = db.Column('HR_ID', db.Integer, ForeignKey('Staff.Staff_ID'))
    
    def json(self):
        dto = {
            'listing_id': self.listing_id,
            'listing_name': self.listing_name,
            'listing_description': self.listing_description,
            'dept': self.dept,
            'deadline': self.deadline.strftime('%Y-%m-%d') if self.deadline is not None else None,
            'hr_id': self.hr_id
        }
        return dto

class RoleSkill(db.Model):
    __tablename__ = 'Role_Skill'

    role_id = db.Column('Role_ID', db.Integer, ForeignKey('Role.Role_ID'), primary_key=True)
    skill_id = db.Column('Skill_ID', db.Integer, ForeignKey('Skill.Skill_ID'), primary_key=True)

    def json(self):
        dto = {
            'role_id': self.role_id,
            'skill_id': self.skill_id
        }
        return dto

class ListingSkill(db.Model):
    __tablename__ = 'Listing_Skill'

    listing_id = db.Column('Listing_ID', db.Integer, ForeignKey('Listing.Listing_ID'), primary_key=True)
    skill_id = db.Column('Skill_ID', db.Integer, ForeignKey('Skill.Skill_ID'), primary_key=True)

    def json(self):
        dto = {
            'listing_id': self.listing_id,
            'skill_id': self.skill_id
        }
        return dto

class StaffSkill(db.Model):
    __tablename__ = 'Staff_Skill'

    staff_id = db.Column('Staff_ID', db.Integer, ForeignKey('Staff.Staff_ID'), primary_key=True, nullable=False)
    skill_id = db.Column('Skill_ID', db.Integer, ForeignKey('Skill.Skill_ID'), primary_key=True, nullable=False)

    def json(self):
        dto = {
            'staff_id': self.staff_id,
            'skill_id': self.skill_id
        }
        return dto
    
class Application(db.Model):
    __tablename__ = 'Application'

    application_id = db.Column('Application_ID', db.Integer, primary_key=True, autoincrement=True)
    staff_id = db.Column('Staff_ID', db.Integer, ForeignKey('Staff.Staff_ID'), nullable=False)
    staff_name = db.Column('Staff_Name', db.String(100))
    listing_id = db.Column('Listing_ID', db.Integer, ForeignKey('Listing.Listing_ID'), nullable=False)
    date_applied = db.Column('Date_Applied', db.Date, nullable=False)

    def json(self):
        dto = {
            'application_id': self.application_id,
            'staff_id': self.staff_id,
            'staff_name': self.staff_name,
            'listing_id': self.listing_id,
            'date_applied': self.date_applied.strftime('%Y-%m-%d'),  # Format date as string
        }
        return dto
