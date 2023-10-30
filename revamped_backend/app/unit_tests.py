import unittest
from flask import Flask
from models import Staff,Role,RoleSkill,ListingSkill,StaffSkill,Application, Listing, db
from datetime import datetime

import json
from os import environ

class TestRole(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3" #TestDatabase
        db.init_app(self.app)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_to_json_Role(self):
        s1 = Role(role_id=1, 
                   role_name="Account Manager", 
                   role_description="The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily."
                   )
        

        self.assertEqual(s1.json(), {
            'role_id':1, 
            'role_name':"Account Manager", 
            'role_description':"The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily."
        })

   

    
    
    def test_get_all_role_skill(self):
        response = self.app.get('/role_skill')
        data = response.get_json()

        # Ensure the response is 201
        self.assertEqual(response.status_code, 201)
        
        # Check that the response is a dictionary (which it should be, based on your route)
        self.assertIsInstance(data["data"], dict)

        # Optionally, for further accuracy, check a few known role-skills from your data
        # to ensure they are correctly returned:
        # For example, if role_id=1 has skills 1, 10, and 12:
        self.assertIn(1, data["data"])
        self.assertListEqual(data["data"][1], [1, 10, 12])


    def test_RoleSkill(self):
        
        role_id = 1
        response = self.app.get(f'/role_skill/{role_id}')
        data = response.get_json()

        # Ensure the response is 200
        self.assertEqual(response.status_code, 200)
        # Check that the returned role_id matches the requested one
        self.assertEqual(data["data"]["role_id"], role_id)
        # For further accuracy, you can also check that the skill_ids match expected values
        expected_skill_ids = [1, 10, 12, 14, 15, 20, 21, 25, 51, 53, 54, 61, 72]
        self.assertListEqual(data["data"]["skill_ids"], expected_skill_ids)


    def test_invalid_role_id(self):
        # Using a role_id that does not exist or has no skills
        role_id = 99999  # assuming this ID does not exist
        response = self.app.get(f'/role_skill/{role_id}')
        data = response.get_json()

        # Ensure the response is 404
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["message"], "No skills found for the given role id.")


    
    def test_get_all_roles(self):
        # Make a request to get all roles
        response = self.client.get("/roles")
        self.assertEqual(response.status_code, 200)
        
        # Check the response data
        data = json.loads(response.data)
        self.assertEqual(len(data['data']), 22)  
        
        self.assertEqual(data['data'][0]['role_name'], "Account Manager")
        self.assertEqual(data['data'][1]['role_name'], "Admin Executive")
        self.assertEqual(data['data'][2]['role_name'], "Call Centre")
        self.assertEqual(data['data'][3]['role_name'], "Consultancy Director")
        self.assertEqual(data['data'][4]['role_name'], "Consultant")
        self.assertEqual(data['data'][5]['role_name'], "Developer")
        self.assertEqual(data['data'][6]['role_name'], "Engineering Director")
        self.assertEqual(data['data'][7]['role_name'], "Finance Executive")
        self.assertEqual(data['data'][8]['role_name'], "Finance Director")
        self.assertEqual(data['data'][9]['role_name'], "Finance Manager")
        self.assertEqual(data['data'][10]['role_name'], "HR Director")
        self.assertEqual(data['data'][11]['role_name'], "HR Executive")
        self.assertEqual(data['data'][12]['role_name'], "IT Analyst")
        self.assertEqual(data['data'][13]['role_name'], "IT Director")
        self.assertEqual(data['data'][14]['role_name'], "Junior Engineer")
        self.assertEqual(data['data'][15]['role_name'], "L&D Executive")
        self.assertEqual(data['data'][16]['role_name'], "Ops Planning Exec")
        self.assertEqual(data['data'][17]['role_name'], "Sales Director")
        self.assertEqual(data['data'][18]['role_name'], "Sales Manager")
        self.assertEqual(data['data'][19]['role_name'], "Senior Engineer")
        self.assertEqual(data['data'][20]['role_name'], "Solutioning Director")
        self.assertEqual(data['data'][21]['role_name'], "Support Engineer")
        
        

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


class TestListingSkill(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3" #TestDatabase
        db.init_app(self.app)
        self.client = self.app.test_client()

        self.ctx = self.app.app_context()
        self.ctx.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()


    def test_create_listing(self):
        response = self.client.post('/create_listing', json={
            'listing_name': 'Account Manager',
            'listing_description': "The Account Manager acts as a key point of contact between an organisation and its clients. He/She possesses thorough product knowledge and oversees product and/or service sales. He works with customers to identify their wants and prepares reports by collecting, analysing, and summarising sales information. He contacts existing customers to discuss and give recommendations on how specific products or services can meet their needs. He maintains customer relationships to strategically place new products and drive sales for long-term growth. He works in a fast-paced and dynamic environment, and travels frequently to clients' premises for meetings. He is familiar with client relationship management and sales tools. He is knowledgeable of the organisation's products and services, as well as trends, developments and challenges of the industry domain. The Sales Account Manager is a resourceful, people-focused and persistent individual, who takes rejection as a personal challenge to succeed when given opportunity. He appreciates the value of long lasting relationships and prioritises efforts to build trust with existing and potential customers. He exhibits good listening skills and is able to establish rapport with customers and team members alike easily.",
            'deadline': '2023-11-10',
            'dept': 'Finance',
            'hr_id': 190019,
            'listing_skill': [1, 10,12,14,15,20,21,25,51,53,54,61,72]
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['data']['listing_name'], 'Account Manager')

    def test_get_all_listings(self):
        response = self.client.get('/listings')
        self.assertEqual(response.status_code, 200)

    def test_get_listing(self):
        listing = Listing(listing_name='Test Listing', listing_description='Test Description', dept='HR', deadline='2023-10-30', hr_id=190019)
        db.session.add(listing)
        db.session.commit()
        response = self.client.get(f'/listings/{listing.listing_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['listing_name'], 'Test Listing')

    def test_update_listing(self):
        listing = Listing(listing_name='Test Listing', listing_description='Test Description', dept='HR', deadline='2023-10-30', hr_id=190019)
        db.session.add(listing)
        db.session.commit()
        response = self.client.put(f'/update_listing/{listing.listing_id}', json={
            'listing_name': 'Updated Test Listing',
            'listing_description': 'Updated Test Description',
            'dept': 'Finance',
            'deadline': '2023-11-30',
            'listing_skill': [1,2,3]
        })
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['listing_name'], 'Updated Test Listing')

    def test_get_skills_by_listing(self):
        listing = Listing(listing_name='Test Listing', listing_description='Test Description', dept='HR', deadline='2023-10-30', hr_id=1)
        db.session.add(listing)
        db.session.commit()
        listing_skill = ListingSkill(listing_id=listing.listing_id, skill_id=1)
        db.session.add(listing_skill)
        db.session.commit()
        response = self.client.get(f'/listing_skill/{listing.listing_id}')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertIn(1, data['data']['skill_ids'])


class TestStaffSkill(unittest.TestCase):
        
            def setUp(self):
                self.app = Flask(__name__)
                self.app.config['TESTING'] = True
                self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://root@localhost:3306/spm3" #TestDatabase
                db.init_app(self.app)
                self.client = self.app.test_client()
        
                self.ctx = self.app.app_context()
                self.ctx.push()
                db.create_all()
        
            def tearDown(self):
                db.session.remove()
                db.drop_all()
                self.ctx.pop()
            
            def test_to_json_StaffSkill(self):
                s1 = StaffSkill(staff_id=1, 
                        skill_id=1
                        )
                
        
                self.assertEqual(s1.json(), {
                    'staff_id':140001, 
                    'skill_id':[1,12,23,26,37,51,54,79]
                })
        
            def test_get_skills_by_staff(self):
                
        
                # Make a request to get skills by staff ID
                response = self.client.get("/staff_skill/140001")
                self.assertEqual(response.status_code, 200)
        
                # Check the response data
                data = json.loads(response.data)
                self.assertEqual(data['data']['staff_id'], 140001)
                # Assertions for the skills associated with staff_id=140001
        
                # Test for a non-existent staff
                response = self.client.get("/staff_skill/23")  # Staff ID 23 does not exist based on the image
                self.assertEqual(response.status_code, 404)
                data = json.loads(response.data)
                self.assertEqual(data['message'], "No skills found for the given staff id.")


class TestApplication(unittest.TestCase):
    def setUp(self):
            self.app = Flask(__name__)
            self.app.config['TESTING'] = True
            self.app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('dbURL') or "mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm3"
            db.init_app(self.app)
            self.client = self.app.test_client()

            self.ctx = self.app.app_context()
            self.ctx.push()
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.ctx.pop()

    def test_apply_for_listing(self):
        # Sample data for testing the POST method
        data = {
            "staff_id": 140002,
            "listing_id": 1,
            "staff_name": "Susan Goh"
        }
        response = self.client.post('/apply', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_applications(self):
        response = self.client.get('/applications')
        self.assertEqual(response.status_code, 200)  # Assuming that there's always at least one application in your test database setup

    def test_get_applications_by_listing(self):
        listing_id = 1  # Assuming a listing with ID 1 exists in your test database setup
        response = self.client.get(f'/listings/{listing_id}/applications')
        self.assertEqual(response.status_code, 200)

    def test_get_application_by_id(self):
        application_id = 1  # Assuming an application with ID 1 exists in your test database setup
        response = self.client.get(f'/applications/{application_id}')
        self.assertEqual(response.status_code, 200)


class TestStaff(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
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
        s1 = Staff(staff_id=1, 
                   staff_fname="John", 
                   staff_lname="Doe", 
                   dept="IT", 
                   country="USA",
                   email="john.doe@gmail.com",
                   role=1
                   )

        self.assertEqual(s1.json(), {
            'staff_id': 1,
            'staff_fname': 'John',
            'staff_lname': 'Doe',
            'dept': 'IT',
            'country': 'USA',
            'email': 'john.doe@gmail.com',
            'role': 1
        })
        

    # def test_get_all_staff(self):
    #     with self.app.app_context():
    #         # Add a sample staff record to the database
    #         staff = Staff(staff_id='1234',staff_fname='John', staff_lname='Doe', 
    #                     dept='HR', country='USA', email='john.doe@example.com')
    #         db.session.add(staff)
    #         db.session.commit()

    #     # Send a GET request to the /staffs endpoint
    #     response = self.client.get('/staffs')
    #     print(response.data)
    #     data = json.loads(response.data.decode('utf-8'))

    #     # Check the response status code and data
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(len(data['data']), 1)
    #     self.assertEqual(data['data'][0]['staff_fname'], 'John')
    #     self.assertEqual(data['data'][0]['staff_lname'], 'Doe')
    #     self.assertEqual(data['data'][0]['dept'], 'HR')
    #     self.assertEqual(data['data'][0]['country'], 'USA')
    #     self.assertEqual(data['data'][0]['email'], 'john.doe@example.com')
    #     self.assertEqual(data['data'][0]['role'], 1)

    # def test_get_staff_by_id(self):
        # Add a sample staff record to the database
        with self.app.app_context():
            staff = Staff(staff_id=2, staff_fname='John', staff_lname='Doe', 
                        dept='HR', country='USA', email='jonDoe@gmail.com', role=1)
            db.session.add(staff)
            db.session.commit()

        response = self.client.get('/staffs/2')
        print(response.data)
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['data']['staff_fname'], 'John')
        self.assertEqual(data['data']['staff_lname'], 'Doe')
        self.assertEqual(data['data']['dept'], 'HR')
        self.assertEqual(data['data']['country'], 'USA')
        self.assertEqual(data['data']['email'], 'jonDoe@gmail.com')
        self.assertEqual(data['data']['role'], 1)
        
if __name__ == "__main__":
    unittest.main()
