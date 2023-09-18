from unittest import TestCase
from models import db, Cupcake
from app import app
import unittest

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_ECHO'] = False
app.config['TESTING'] = True  # Make Flask errors be real errors

CUPCAKE_DATA = {
    "flavor": "TestFlavor",
    "size": "TestSize",
    "rating": 5,
    "image": "http://test.com/cupcake.jpg"
}

CUPCAKE_DATA_2 = {
    "flavor": "TestFlavor2",
    "size": "TestSize2",
    "rating": 10,
    "image": "http://test.com/cupcake2.jpg"
}

class CupcakeViewsTestCase(TestCase):
    """Tests for views of API."""

    def setUp(self):
        """Before each test, set up test client and make demo data."""
        app.config['TESTING'] = True
        self.client = app.test_client()
        
        with app.app_context():
            Cupcake.query.delete()
            cupcake = Cupcake(**CUPCAKE_DATA)
            db.session.add(cupcake)
            db.session.commit()
            self.cupcake = db.session.get(Cupcake, cupcake.id)  # Re-query the cupcake instance after committing

    @classmethod
    def setUpClass(cls):
        """Once before all tests, drop database and re-create it."""
        with app.app_context():
            db.drop_all()
            db.create_all()

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            resp = client.get("/api/cupcakes")

            self.assertEqual(resp.status_code, 200)

            data = resp.json
            self.assertEqual(data, {
                "cupcakes": [
                    {
                        "id": self.cupcake.id,
                        "flavor": "TestFlavor",
                        "size": "TestSize",
                        "rating": 5,
                        "image": "http://test.com/cupcake.jpg"
                    }
                ]
            })

    def test_get_cupcake(self):
        with app.test_client() as client:
            url = f"/api/cupcakes/{self.cupcake.id}"
            resp = client.get(url)

            self.assertEqual(resp.status_code, 200)
            data = resp.json
            self.assertEqual(data, {
                "cupcake": {
                    "id": self.cupcake.id,
                    "flavor": "TestFlavor",
                    "size": "TestSize",
                    "rating": 5,
                    "image": "http://test.com/cupcake.jpg"
                }
            })

    def test_update_cupcake(self):
        res = self.client.patch(f"/api/cupcakes/{self.cupcake.id}", 
                                json={"flavor": "new_flavor", "size": "new_size", "rating": 1.5, "image": "new_image.jpg"})
        json = res.get_json()
    
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json, {
            "cupcake": {
                "id": self.cupcake.id,
                "flavor": "new_flavor",
                "size": "new_size",
                "rating": 1.5,
                "image": "new_image.jpg"
            }
        })
    
    def test_delete_cupcake(self):
        res = self.client.delete(f"/api/cupcakes/{self.cupcake.id}")
        json = res.get_json()
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(json, {"message": "Deleted"})


    def test_create_cupcake(self):
        with app.test_client() as client:
            url = "/api/cupcakes"
            resp = client.post(url, json=CUPCAKE_DATA_2)

            self.assertEqual(resp.status_code, 201)

            data = resp.json

            # don't know what ID we'll get, make sure it's an int & normalize
            self.assertIsInstance(data['cupcake']['id'], int)
            del data['cupcake']['id']

            self.assertEqual(data, {
                "cupcake": {
                    "flavor": "TestFlavor2",
                    "size": "TestSize2",
                    "rating": 10,
                    "image": "http://test.com/cupcake2.jpg"
                }
            })

            self.assertEqual(Cupcake.query.count(), 2)

if __name__ == '__main__':
    unittest.main()
