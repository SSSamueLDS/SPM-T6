from datetime import date
import unittest
from flask_testing import TestCase
import json
from application import app, db, Application

class ApplicationTestCase(TestCase):

    # This method will be called before every test
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Using in-memory SQLite for tests
        return app

    # This method will be called before the first test
    def setUp(self):
        db.create_all()

    # This method will be called after the last test
    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_apply_for_listing(self):
        # Assuming a staff_id of 1 and a listing_id of 1 for testing purposes
        response = self.client.post('/apply', json={'staff_id': 1, 'listing_id': 1, 'staff_name': 'Test Staff'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertTrue('staff_id' in data)

    def test_get_all_applications(self):
        response = self.client.get('/applications')
        self.assertEqual(response.status_code, 404)  # Initially, there will be no applications

    def test_get_applications_by_listing(self):
        # Create a dummy application for testing
        application = Application(staff_id=1, listing_id=1, staff_name='Test Staff', date_applied=date.today())
        db.session.add(application)
        db.session.commit()
        
        response = self.client.get('/listings/1/applications')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in data)

    def test_get_application_by_id(self):
        # Create a dummy application for testing
        application = Application(staff_id=1, listing_id=1, staff_name='Test Staff', date_applied=date.today())
        db.session.add(application)
        db.session.commit()

        response = self.client.get('/applications/1')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('data' in data)


if __name__ == '__main__':
    unittest.main()


