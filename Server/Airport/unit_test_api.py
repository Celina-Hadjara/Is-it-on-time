import unittest
from flask_testing import TestCase
from flask import json

# Importez l'objet 'app' de votre application Flask ici
from app import app


def create_app():
    app.config['TESTING'] = True
    return app


class TestApp(TestCase):

    def test_airport_dep_list(self):
        response = self.client.get("/api/airport_dep_list")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("airport_list" in data)
        self.assertIsInstance(data["airport_list"], list)

    def test_airport_dest_list(self):
        response = self.client.get("/api/airport_dest_list")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("airport_list" in data)
        self.assertIsInstance(data["airport_list"], list)

    def test_airport_dep_delay_trend(self):
        response = self.client.get("/api/airport_dep_delay_trend", query_string={"airport_code": "John F. Kennedy International Airport"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("mean_delay" in data)
        self.assertIsInstance(data["mean_delay"], list)

    def test_airport_arr_delay_trend(self):
        response = self.client.get("/api/airport_arr_delay_trend", query_string={"airport_code": "John F. Kennedy International Airport"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertTrue("mean_delay" in data)
        self.assertIsInstance(data["mean_delay"], list)


if __name__ == "__main__":
    unittest.main()
