import unittest
import json
from main import app, db, Application, Staff, Skill, Role, RoleSkill, StaffSkill, AccessControl, Listing, ListingSkill
from datetime import date

class TestApplication(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.staff_id = 140002
        self.listing_id = 5
        self.staff_name = "susan goh"

    def tearDown(self):
        db.session.query(Application).delete()
        db.session.commit()

    def test_apply_for_listing(self):
        data = {
            "staff_id": self.staff_id,
            "listing_id": self.listing_id,
            "staff_name": self.staff_name
        }
        response = self.app.post('/apply', json=data)
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
        self.assertTrue(data['staff_id'] == self.staff_id)
        self.assertTrue(data['listing_id'] == self.listing_id)
        self.assertTrue(data['staff_name'] == self.staff_name)
        
if __name__ == '__main__':
    with app.app_context():
        unittest.main()