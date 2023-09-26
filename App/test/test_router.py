import unittest
from unittest.mock import patch
from flask import json
from App.app.router import app

class RouterTestCase(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.client = app.test_client()

    def test_health_check(self):
        response = self.client.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {"status": "healthy", "container": "unknown"})

    @patch('app.app.fetch_secret')
    def test_get_secret_valid(self, mock_fetch_secret):
        mock_fetch_secret.return_value = 'mock_secret'
        response = self.client.get('/secret?codeName=thedoctor', headers={'Authorization': 'Bearer default_token'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json.loads(response.data.decode()), {'secretCode': 'mock_secret'})

    @patch('app.app.fetch_secret')
    def test_get_secret_invalid(self, mock_fetch_secret):
        mock_fetch_secret.return_value = None
        response = self.client.get('/secret?codeName=wrongdoctor', headers={'Authorization': 'Bearer default_token'})
        self.assertEqual(response.status_code, 403)

    def test_get_secret_no_token(self):
        response = self.client.get('/secret?codeName=thedoctor')
        self.assertEqual(response.status_code, 403)

    # Add a test for the /token endpoint
    def test_get_token(self):
        response = self.client.get('/token')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('token' in json.loads(response.data.decode()))

if __name__ == '__main__':
    unittest.main()
