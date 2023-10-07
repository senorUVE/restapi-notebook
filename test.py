import unittest
import requests
import json

class TestAPI(unittest.TestCase):
    BASE_URL = 'http://localhost:5000/api/v1/notebook/'

    def test_get_all(self):
        r = requests.get(self.BASE_URL)
        self.assertEqual(r.status_code, 200)

    def test_post_contact(self):
        contact = {
            "full_name": "John Doe",
            "phone": "+123456789",
            "email": "john@example.com"
        }
        r = requests.post(self.BASE_URL, json=contact)
        self.assertEqual(r.status_code, 201)

    # Добавьте другие тестовые кейсы...

if __name__ == '__main__':
    unittest.main()
