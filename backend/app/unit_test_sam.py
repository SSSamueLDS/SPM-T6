import unittest
import json
from main import app

class TestMainRoutes(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    def test_get_all_staff_skill(self):
        response = self.app.get('/staff_skill')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('data', data)
        self.assertIsInstance(data['data'], dict)

    def test_get_staff_by_id(self):
        response = self.app.get('/staffs/140002')
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertIn('data', data)
            self.assertIsInstance(data['data'], dict)
        elif response.status_code == 404:
            self.assertIn('message', data)
            self.assertEqual(data['code'], 404)

    def test_get_all_depts(self):
        response = self.app.get('/staffs/dept')
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertIn('data', data)
            self.assertIsInstance(data['data'], list)
        elif response.status_code == 404:
            self.assertIn('message', data)
            self.assertEqual(data['code'], 404)

    def test_get_staff_skills(self):
        response = self.app.get('/staffs/skills/17')
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertIn('data', data)
            self.assertIsInstance(data['data'], list)
        elif response.status_code == 404:
            self.assertIn('message', data)
            self.assertEqual(data['code'], 404)

    def test_get_staff_skilldisplay(self):
        response = self.app.get('/staffs/display_skills/140002')
        data = json.loads(response.data)
        if response.status_code == 200:
            self.assertIn('data', data)
            self.assertIsInstance(data['data'], dict)
        elif response.status_code == 404:
            self.assertIn('message', data)
            self.assertEqual(data['code'], 404)
            
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

    def test_get_all_roles(self):
        response = self.app.get('/roles')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('data', data)
        self.assertTrue(isinstance(data['data'], list))






if __name__ == '__main__':
    unittest.main()
