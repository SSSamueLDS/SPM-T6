# The above class is a unit test class for testing the database tables in a Flask application.
import unittest
from flask import Flask
from models import Staff,Role,RoleSkill,ListingSkill,StaffSkill,Application, Listing, db, AccessControl, Skill
from datetime import datetime
import json
from sqlalchemy.orm import Session
# from sqlalchemy import create_engine, text
# from populate_data import load_data_into_db
from main import app, db
from flask_testing import TestCase


class TestStaff(TestCase):

    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        
        # This is the potential fix
        if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        return app
    
    def setUp(self):
        with self.app.app_context():
            db.create_all()

            access1 = AccessControl(access_id=1, access_control_name="Admin")
            access2 = AccessControl(access_id=2, access_control_name="Staff")
            db.session.add(access1)
            db.session.add(access2)
            db.session.commit()

            staff1 = Staff(staff_id=10001, staff_fname="John", staff_lname="Doe", dept="IT", country="Singapore", email="john.doe@example.com", role=1)
            staff2 = Staff(staff_id=10002,staff_fname="Jane", staff_lname="Doe", dept="IT", country="Singapore", email="jane.smith@example.com", role=2)

            db.session.add(staff1)
            db.session.add(staff2)
            db.session.commit()

            skill1 = Skill(skill_id=1, skill_name="Python", skill_desc="Python is a programming language")
            skill2 = Skill(skill_id=2, skill_name="Java", skill_desc="Java is a programming language")
            skill3 = Skill(skill_id=3, skill_name="C++", skill_desc="C++ is a programming language")
            skill4 = Skill(skill_id=4, skill_name="C#", skill_desc="C# is a programming language")
            
            db.session.add(skill1)
            db.session.add(skill2)
            db.session.add(skill3)
            db.session.add(skill4)
            db.session.commit()

            # Now, assign skills to staff1
            staff_skill1 = StaffSkill(staff_id=10001, skill_id=skill1.skill_id)
            staff_skill2 = StaffSkill(staff_id=10001, skill_id=skill2.skill_id)
            staff_skill3 = StaffSkill(staff_id=10001, skill_id=skill3.skill_id)
            staff_skill4 = StaffSkill(staff_id=10002, skill_id=skill4.skill_id)
            staff_skill5 = StaffSkill(staff_id=10002, skill_id=skill2.skill_id)

            # Add StaffSkill instances to session
            db.session.add(staff_skill1)
            db.session.add(staff_skill2)
            db.session.add(staff_skill3)
            db.session.add(staff_skill4)
            db.session.add(staff_skill5)

            
            # Final commit to save everything
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():  # Also for teardown
            db.session.remove()
            db.drop_all()

    def test_get_all_staff(self):
        with self.app.app_context():
            response = self.client.get('/staffs')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data['data']), 2)
            # Now use the json method from your Staff instances for comparison
            staff1_data = Staff.query.filter_by(staff_id=10001).first().json()
            staff2_data = Staff.query.filter_by(staff_id=10002).first().json()
            self.assertIn(staff1_data, data['data'])
            self.assertIn(staff2_data, data['data'])

    def test_get_staff_by_id(self):
        with self.app.app_context():
            response = self.client.get('/staffs/10001')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(data['data']['staff_id'], 10001)
            self.assertEqual(data['data']['staff_fname'], "John")
            self.assertEqual(data['data']['staff_lname'], "Doe")
            self.assertEqual(data['data']['dept'], "IT")
            self.assertEqual(data['data']['country'], "Singapore")
            self.assertEqual(data['data']['email'], "john.doe@example.com")
            self.assertEqual(data['data']['role'], 1)

    def test_get_all_depts(self):
        with self.app.app_context():
            response = self.client.get('/staffs/dept')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            self.assertEqual(len(data['data']), 1)
            self.assertEqual(data['data'], ["IT"])

    def test_get_staff_skills(self):
        with self.app.app_context():
            response = self.client.get('/staffs/skills/10001')
            self.assertEqual(response.status_code, 200)
            data = response.get_json()
            expected_skill_ids = [1, 2, 3]
            self.assertEqual(data['data'], expected_skill_ids)

    def test_get_all_staff_skill(self):
        """ Test retrieval of all staff skills mapping. """
        with self.app.app_context():
           
            response = self.client.get("/staff_skill")
            self.assertEqual(response.status_code, 201)
            data = response.get_json()
            

            expected_map = {
                '10001': [1, 2, 3],
                '10002': [4, 2]
                
            }
            
            # Check if the returned staff-skill mapping is correct
            self.assertEqual(data['data'], expected_map)

    def test_get_staff_skilldisplay(self):
        with self.app.app_context():
            response = self.client.get("/staffs/display_skills/10001")
            self.assertEqual(response.status_code, 200)
            data = response.get_json()

            # We expect to get back a dictionary where the keys are skill IDs
            # and the values are skill names for the staff with ID 10001.
            expected_skill_map = {
                '1': "Python",
                '2': "Java",
                '3': "C++"
            }
            self.assertDictEqual(data['data'], expected_skill_map)

    def test_get_all_access_control(self):
        with self.app.app_context():
            response = self.client.get('/access_control')
            self.assertEqual(response.status_code, 200)
            data = json.loads(response.data.decode('utf-8'))
            self.assertEqual(len(data['data']), 2)
            # You could add more asserts here to check the content of the returned data
            # For example:
            self.assertEqual(data['data'][0]['access_control_name'], "Admin")
            self.assertEqual(data['data'][1]['access_control_name'], "Staff")


    def test_get_all_access_control_no_data(self):
        with self.app.app_context():
        # Empty the table for this test
            AccessControl.query.delete()
            db.session.commit()
            response = self.client.get('/access_control')
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data.decode('utf-8'))
            self.assertIn("No access control found", data['message'])

class TestSkill(TestCase):
        def create_app(self):
            app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
            app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
            app.config['TESTING'] = True
            
            # This is the potential fix
            if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
                db.init_app(app)
            return app
        
        def setUp(self):
            with self.app.app_context():
                db.create_all()
    
                s1 = Skill(skill_id=1, skill_name="Python", skill_desc="Python is a programming language")
                s2 = Skill(skill_id=2, skill_name="Java", skill_desc="Java is a programming language")
                s3 = Skill(skill_id=3, skill_name="C++", skill_desc="C++ is a programming language")
                s4 = Skill(skill_id=4, skill_name="C#", skill_desc="C# is a programming language")
                db.session.add(s1)
                db.session.add(s2)
                db.session.add(s3)
                db.session.add(s4)
                db.session.commit()
    
        def tearDown(self):
            with self.app.app_context():  # Also for teardown
                db.session.remove()
                db.drop_all()
    
        def test_get_all_skills(self):
            with self.app.app_context():
                response = self.client.get('/skills')
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(len(data['data']), 4)
                # Now use the json method from your Skill instances for comparison
                skill1_data = Skill.query.filter_by(skill_id=1).first().json()
                skill2_data = Skill.query.filter_by(skill_id=2).first().json()
                skill3_data = Skill.query.filter_by(skill_id=3).first().json()
                skill4_data = Skill.query.filter_by(skill_id=4).first().json()
                self.assertIn(skill1_data, data['data'])
                self.assertIn(skill2_data, data['data'])
                self.assertIn(skill3_data, data['data'])
                self.assertIn(skill4_data, data['data'])

        def test_get_skill_by_id(self):
            with self.app.app_context():
                response = self.client.get('/skills/1')
                self.assertEqual(response.status_code, 200)
                data = response.get_json()
                self.assertEqual(data['data']['skill_id'], 1)
                self.assertEqual(data['data']['skill_name'], "Python")

        def test_get_all_skills_empty(self):
            with self.app.app_context():
                Skill.query.delete()
                db.session.commit()
                response = self.client.get('/skills')
                data = json.loads(response.data.decode('utf-8'))
                self.assertEqual(data["code"], 404)
                self.assertIn("No skills found", data['message'])

        def test_get_skill_by_id_not_found(self):
            with self.app.app_context():
                response = self.client.get('/skills/100')
                data = json.loads(response.data.decode('utf-8'))
                # self.assertEqual(response.status_code, 404)
                self.assertIn("No skill found for id 100", data['message'])


class TestRole(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        
        # This is the potential fix
        if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        return app
    
    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def test_get_all_roles_with_data(self):
        r1 = Role(role_name="Developer", role_description="Write code")
        r2 = Role(role_name="Tester", role_description="Test code")
        db.session.add(r1)
        db.session.add(r2)
        db.session.commit()

        response = self.client.get('/roles')
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data'][0]['role_name'], "Developer")
        self.assertEqual(data['data'][1]['role_name'], "Tester")

    def test_get_all_roles_no_data(self):
        response = self.client.get('/roles')
        data = json.loads(response.data.decode('utf-8'))

        self.assertEqual(response.status_code, 404)
        self.assertIn("No roles found", data['message'])

class RoleSkillTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        
        # This is the potential fix
        if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        return app

    def setUp(self):
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
    
    def test_get_skills_by_role_with_data(self):
        role = Role(role_name="Developer", role_description="Write code")
        s1 = Skill(skill_id=1, skill_name="Python", skill_desc="Python is a programming language")
        s2 = Skill(skill_id=2, skill_name="Java", skill_desc="Java is a programming language")
        db.session.add(role)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

        role_skill1 = RoleSkill(role_id=role.role_id, skill_id=s1.skill_id)
        role_skill2 = RoleSkill(role_id=role.role_id, skill_id=s2.skill_id)
        db.session.add(role_skill1)
        db.session.add(role_skill2)
        db.session.commit()

        response = self.client.get('/role_skill/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(data['data']), 2)
        self.assertEqual(data['data']['role_id'], 1)
        self.assertEqual(data['data']['skill_ids'], [1,2])

    def test_get_skills_by_role_empty(self):
        role = Role(role_name="Developer", role_description="Write code")
        db.session.add(role)
        db.session.commit()

        response = self.client.get('/role_skill/1')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data.decode('utf-8'))
        self.assertIn("No skills found for the given role id", data['message'])

    def test_get_all_role_skill_with_data(self):
        role = Role(role_name="Developer", role_description="Write code")
        skill = Skill(skill_name="Python", skill_desc="Python is a programming language")
        db.session.add(role)
        db.session.add(skill)
        db.session.commit()

        role_skill = RoleSkill(role_id=role.role_id, skill_id=skill.skill_id)
        db.session.add(role_skill)
        db.session.commit()

        response = self.client.get('/role_skill')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data.decode('utf-8'))
        self.assertEqual(len(data['data']), 1)

class ListingTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        
        # This is the potential fix
        if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

        role = Role(role_name="HR", role_description="create listing")

        hr = Staff(
            staff_id=1001,
            staff_fname='John',
            staff_lname='Doe',
            dept='IT',
            country='USA',
            email='john.doe@example.com',
            role=1)

        s1 = Skill(skill_name='Python', skill_desc='Python programming language')
        s2 = Skill(skill_name='JavaScript', skill_desc='JavaScript programming language')

        db.session.add(role)
        db.session.add(hr)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()


    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_create_listing_success(self):
        
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1001,
            "listing_skill": [1,2]
        }

        response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_create_listing_no_skills(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": []  # Empty skill list should trigger the error
        }
        
        response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("Please select at least one skill for the listing", response.json['message'])

    def test_create_listing_no_data(self):
        # Assuming the application returns a specific message when no data is provided
        response = self.client.post('/create_listing', data=json.dumps({}),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn("No deadline provided", response.json['message'])

    def test_get_all_listings(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": [1,2]
        }
        
        create_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                content_type='application/json')
        self.assertEqual(create_response.status_code, 201)
        
        response = self.client.get('/listings')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json['data'], list)
        self.assertTrue(len(response.json['data']) > 0)

    def test_update_listing(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": [1,2]
        }

        create_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                        content_type='application/json')
        self.assertEqual(create_response.status_code, 201)

        listing_id = 1
        update_data = {
            "listing_name": "Data Analyst",
            "listing_description": "clean up data",
            "deadline": "2023-12-12",
            "dept": "IT",
            "listing_skill": [1,2]
        }

        response = self.client.put(f'/update_listing/{listing_id}', data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 200)

        updated_listing = Listing.query.get(listing_id)
        self.assertEqual(updated_listing.listing_name, 'Data Analyst')

    def test_update_listing_no_data(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": [1,2]
        }

        create_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                        content_type='application/json')
        self.assertEqual(create_response.status_code, 201)

        response = self.client.put('/update_listing/1', data=json.dumps({}),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_update_listing_invalid_deadline(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": [1,2]
        }

        create_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                        content_type='application/json')
        self.assertEqual(create_response.status_code, 201)

        listing_id = 1
        update_data = {
            "listing_name": "Data Analyst",
            "listing_description": "clean up data",
            "deadline": "2023-02-02",
            "dept": "IT",
            "listing_skill": [1,2]
        }

        response = self.client.put('/update_listing/1', data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['errors'], ['Deadline should not be in the past'])
        
def test_update_listing_missing_fields(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1,
            "listing_skill": [1,2]
        }

        create_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                        content_type='application/json')
        self.assertEqual(create_response.status_code, 201)

        update_data = {
            "listing_name": "Incomplete Data Analyst",
            "listing_description": "",
            "deadline": "2023-12-12",
            "dept": "",
            "listing_skill": ""
        }

        response = self.client.put('/update_listing/1', data=json.dumps(update_data),
                                   content_type='application/json')
        self.assertEqual(response.status_code, 400)

class TestApplication(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
        app.config['TESTING'] = True
        
        # This is the potential fix
        if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
            db.init_app(app)
        return app

    def setUp(self):
        db.create_all()

        role = Role(role_name="HR", role_description="create listing")
        role = Role(role_name="User", role_description="employee in the place")

        hr = Staff(
            staff_id=1001,
            staff_fname='John',
            staff_lname='Doe',
            dept='IT',
            country='USA',
            email='john.doe@example.com',
            role=1)
        
        staff = Staff(
            staff_id=1002,
            staff_fname='Angie',
            staff_lname='Tan',
            dept='IT',
            country='USA',
            email='angie.tan@example.com',
            role=2)

        s1 = Skill(skill_name='Python', skill_desc='Python programming language')
        s2 = Skill(skill_name='JavaScript', skill_desc='JavaScript programming language')

        db.session.add(role)
        db.session.add(hr)
        db.session.add(s1)
        db.session.add(s2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_apply_for_listing(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1001,
            "listing_skill": [1,2]
        }

        post_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                 content_type='application/json')
        
        data = {
            "staff_id": 1002,
            "listing_id": 1,
            "staff_name": "Angie Tan"
        }
        response = self.client.post('/apply', json=data)
        self.assertEqual(response.status_code, 201)

    def test_get_all_applications(self):
        listing_data = {
            "listing_name": "Software Engineer",
            "listing_description": "Write code",
            "deadline": "2023-12-12",
            "dept": "IT",
            "hr_id": 1001,
            "listing_skill": [1,2]
        }

        post_response = self.client.post('/create_listing', data=json.dumps(listing_data),
                                 content_type='application/json')
        
        data = {
            "staff_id": 1002,
            "listing_id": 1,
            "staff_name": "Angie Tan"
        }
        apply_response = self.client.post('/apply', json=data)
        self.assertEqual(apply_response.status_code, 201)

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

if __name__ == "__main__":
    unittest.main()