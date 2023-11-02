import unittest
from flask import Flask
from models import Staff,Role,RoleSkill,ListingSkill,StaffSkill,Application, Listing, db
from datetime import datetime
from sqlalchemy import create_engine, text
from populate_data import load_data_into_db

import json
import os
from os import environ

class TestRole(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = Flask(__name__)
        cls.app.config['TESTING'] = True

        DATABASE_URI = os.environ.get('devdbURL', 'mysql+mysqlconnector://admin:HelloWorld@db-spm.czpo8yl1nyay.us-east-1.rds.amazonaws.com:3306/spm_unit_test')
        cls.app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
        # print("DATABASE_URI in populate_data.py:", DATABASE_URI)
        
        db.init_app(cls.app)
        cls.client = cls.app.test_client()

        cls.ctx = cls.app.app_context()
        cls.ctx.push()
        db.create_all()

        load_data_into_db(DATABASE_URI)

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()
    #     self.ctx.pop()

    def test_access_control_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Access_Control"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Access_Control table")

    def test_staff_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Staff"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Staff table")

    def test_skill_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Skill"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Skill table")

    def test_role_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Role"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Role table")

    def test_listing_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Listing"))
            count = result.scalar()
            self.assertEqual(count, 0, "No data found in Listing table")

    def test_role_skill_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Role_Skill"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Role_Skill table")

    def test_listing_skill_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Listing_Skill"))
            count = result.scalar()
            self.assertEqual(count, 0, "No data found in Listing_Skill table")

    def test_staff_skill_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Staff_Skill"))
            count = result.scalar()
            self.assertGreater(count, 0, "No data found in Staff_Skill table")

    def test_application_table(self):
        with db.engine.connect() as connection:
            result = connection.execute(text("SELECT COUNT(*) FROM Application"))
            count = result.scalar()
            self.assertEqual(count, 0, "No data found in Application table")
if __name__ == "__main__":
    unittest.main()