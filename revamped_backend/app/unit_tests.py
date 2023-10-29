import unittest
import json
from flask import Flask
from models import Staff, db

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
