import unittest
import json
from main import app

class TestMainRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_get_all_staffs(self):
        response = self.app.get('/staffs')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', data)
        self.assertTrue(isinstance(data['data'], list))

    def test_get_all_skills(self):
        response = self.app.get('/skills')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', data)
        self.assertTrue(isinstance(data['data'], list))

    # You can continue writing test cases for other routes

if __name__ == '__main__':
    unittest.main()
