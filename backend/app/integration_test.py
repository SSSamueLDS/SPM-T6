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


# class TestStaff(TestCase):

#     def create_app(self):
#         app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
#         app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {}
#         app.config['TESTING'] = True
        
#         # This is the potential fix
#         if not hasattr(app, 'extensions') or 'sqlalchemy' not in app.extensions:
#             db.init_app(app)
#         return app
    
#     def setUp(self):
#         with self.app.app_context():
#             db.create_all()

#             access1 = AccessControl(access_id=1, access_control_name="Admin")
#             access2 = AccessControl(access_id=2, access_control_name="Staff")
#             db.session.add(access1)
#             db.session.add(access2)
#             db.session.commit()

#             staff1 = Staff(staff_id=10001, staff_fname="John", staff_lname="Doe", dept="IT", country="Singapore", email="john.doe@example.com", role=1)
#             staff2 = Staff(staff_id=10002,staff_fname="Jane", staff_lname="Doe", dept="IT", country="Singapore", email="jane.smith@example.com", role=2)

#             db.session.add(staff1)
#             db.session.add(staff2)
#             db.session.commit()

#             skill1 = Skill(skill_id=1, skill_name="Python", skill_desc="Python is a programming language")
#             skill2 = Skill(skill_id=2, skill_name="Java", skill_desc="Java is a programming language")
#             skill3 = Skill(skill_id=3, skill_name="C++", skill_desc="C++ is a programming language")
#             skill4 = Skill(skill_id=4, skill_name="C#", skill_desc="C# is a programming language")
            
#             db.session.add(skill1)
#             db.session.add(skill2)
#             db.session.add(skill3)
#             db.session.add(skill4)
#             db.session.commit()

#             # Now, assign skills to staff1
#             staff_skill1 = StaffSkill(staff_id=10001, skill_id=skill1.skill_id)
#             staff_skill2 = StaffSkill(staff_id=10001, skill_id=skill2.skill_id)
#             staff_skill3 = StaffSkill(staff_id=10001, skill_id=skill3.skill_id)
#             staff_skill4 = StaffSkill(staff_id=10002, skill_id=skill4.skill_id)
#             staff_skill5 = StaffSkill(staff_id=10002, skill_id=skill2.skill_id)

#             # Add StaffSkill instances to session
#             db.session.add(staff_skill1)
#             db.session.add(staff_skill2)
#             db.session.add(staff_skill3)
#             db.session.add(staff_skill4)
#             db.session.add(staff_skill5)

            
#             # Final commit to save everything
#             db.session.commit()

#     def tearDown(self):
#         with self.app.app_context():  # Also for teardown
#             db.session.remove()
#             db.drop_all()

#     def test_get_all_staff(self):
#         with self.app.app_context():
#             response = self.client.get('/staffs')
#             self.assertEqual(response.status_code, 200)
#             data = response.get_json()
#             self.assertEqual(len(data['data']), 2)
#             # Now use the json method from your Staff instances for comparison
#             staff1_data = Staff.query.filter_by(staff_id=10001).first().json()
#             staff2_data = Staff.query.filter_by(staff_id=10002).first().json()
#             self.assertIn(staff1_data, data['data'])
#             self.assertIn(staff2_data, data['data'])

#     def test_get_staff_by_id(self):
#         with self.app.app_context():
#             response = self.client.get('/staffs/10001')
#             self.assertEqual(response.status_code, 200)
#             data = response.get_json()
#             self.assertEqual(data['data']['staff_id'], 10001)
#             self.assertEqual(data['data']['staff_fname'], "John")
#             self.assertEqual(data['data']['staff_lname'], "Doe")
#             self.assertEqual(data['data']['dept'], "IT")
#             self.assertEqual(data['data']['country'], "Singapore")
#             self.assertEqual(data['data']['email'], "john.doe@example.com")
#             self.assertEqual(data['data']['role'], 1)

#     def test_get_all_depts(self):
#         with self.app.app_context():
#             response = self.client.get('/staffs/dept')
#             self.assertEqual(response.status_code, 200)
#             data = response.get_json()
#             self.assertEqual(len(data['data']), 1)
#             self.assertEqual(data['data'], ["IT"])

#     def test_get_staff_skills(self):
#         with self.app.app_context():
#             response = self.client.get('/staffs/skills/10001')
#             self.assertEqual(response.status_code, 200)
#             data = response.get_json()
#             expected_skill_ids = [1, 2, 3]
#             self.assertEqual(data['data'], expected_skill_ids)

#     def test_get_all_staff_skill(self):
#         """ Test retrieval of all staff skills mapping. """
#         with self.app.app_context():
           
#             response = self.client.get("/staff_skill")
#             self.assertEqual(response.status_code, 201)
#             data = response.get_json()
            

#             expected_map = {
#                 '10001': [1, 2, 3],
#                 '10002': [4, 2]
                
#             }
            
#             # Check if the returned staff-skill mapping is correct
#             self.assertEqual(data['data'], expected_map)

    # def test_get_staff_skilldisplay(self):
    #     with self.app.app_context():
    #         response = self.client.get("/staffs/display_skills/10001")
    #         self.assertEqual(response.status_code, 200)
    #         data = response.get_json()

    #         # We expect to get back a dictionary where the keys are skill IDs
    #         # and the values are skill names for the staff with ID 10001.
    #         expected_skill_map = {
    #             '1': "Python",
    #             '2': "Java",
    #             '3': "C++"
    #         }
    #         self.assertDictEqual(data['data'], expected_skill_map)

    # def test_get_all_access_control(self):
    #     with self.app.app_context():
    #         response = self.client.get('/access_control')
    #         self.assertEqual(response.status_code, 200)
    #         data = json.loads(response.data.decode('utf-8'))
    #         self.assertEqual(len(data['data']), 2)
    #         # You could add more asserts here to check the content of the returned data
    #         # For example:
    #         self.assertEqual(data['data'][0]['access_control_name'], "Admin")
    #         self.assertEqual(data['data'][1]['access_control_name'], "Staff")


    # def test_get_all_access_control_no_data(self):
    #     with self.app.app_context():
    #     # Empty the table for this test
    #         AccessControl.query.delete()
    #         db.session.commit()
    #         response = self.client.get('/access_control')
    #         self.assertEqual(response.status_code, 404)
    #         data = json.loads(response.data.decode('utf-8'))
    #         self.assertIn("No access control found", data['message'])

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
        
                                                
if __name__ == "__main__":
    unittest.main()