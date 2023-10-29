import unittest
from flask import Flask
from models import Staff,Role,RoleSkill,ListingSkill,StaffSkill,Application, db
from datetime import datetime

import json
from os import environ

class populateTestDatabase(unittest.TestCase):
    
    def setUp(self):
            self.app = Flask(__name__)
            self.app.config['TESTING'] = True
            self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3" #TestDatabase(?)
            db.init_app(self.app)
            self.client = self.app.test_client()

            self.ctx = self.app.app_context()
            self.ctx.push()
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

class TestRole(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3" #TestDatabase(?)
        db.init_app(self.app)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_to_json(self):
        s1 = Role(role_id=1, 
                   role_name="Account Manager", 
                   role_description="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily."
                   )

        self.assertEqual(s1.json(), {
            'role_id':1, 
            'role_name':"Account Manager", 
            'role_description':"The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily."
        })
    
    def test_get_all_roles(self):
        # Make a request to get all roles
        response = self.client.get("/roles")
        self.assertEqual(response.status_code, 200)
        
        # Check the response data
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 22)  
        
        # self.assertEqual(data['data'][0]['role_name'], "Account Manager")
        # self.assertEqual(data['data'][1]['role_name'], "Admin Executive")
        

    def test_skills_by_role(self):
        # This test is dependent on the existence of RoleSkill data. 
        # If the provided image does not include this data, this test might not be valid.

        # Make a request to get skills by role ID
        response = self.client.get("/role_skill/1")
        self.assertEqual(response.status_code, 200)

        # Check the response data
        data = json.loads(response.data)
        self.assertEqual(data['data']['role_id'], 1)
        # Assertions for the skills associated with role_id=1

        # Test for a non-existent role
        response = self.client.get("/role_skill/23")  # Role ID 23 does not exist based on the image
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['message'], "No skills found for the given role id.")

    

class TestRoleSkill(unittest.TestCase):


class TestListingSkill(unittest.TestCase):

class TestStaffSkill(unittest.TestCase):

class TestApplication(unittest.TestCase):