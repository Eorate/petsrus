# coding=utf-8
import unittest

from datetime import date

from petsrus.petsrus import app
from petsrus.models.models import Pet
from petsrus.views.main import session


class PetsRUsTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.session = session

    def tearDown(self):
        self.session.close()

    def test_index(self):
        """Test GET /"""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Index Page" in response.get_data(as_text=True))

    def test_register_user(self):
        """Test POST /register"""
        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        # We should be back in the index page
        self.assertTrue("Index Page" in response.get_data(as_text=True))
        self.assertTrue("Thanks for registering" in response.get_data(as_text=True))

    def test_register_validate_username(self):
        """Test username validation"""
        response = self.client.post(
            "/register",
            data=dict(
                username="",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter your username" in response.get_data(as_text=True))

        response = self.client.post(
            "/register",
            data=dict(
                username="th",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Username must be between 4 to 25 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/register",
            data=dict(
                username="thrainthrainthrainthrainthrain",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Username must be between 4 to 25 characters in length"
            in response.get_data(as_text=True)
        )

    def test_register_validate_email_address(self):
        """Test email address validation"""
        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter your email" in response.get_data(as_text=True))

        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a valid email address" in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a valid email address" in response.get_data(as_text=True)
        )

    def test_register_validate_password(self):
        """Test password validation"""
        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aede",
                confirm_password="",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Passwords must match" in response.get_data(as_text=True))
        self.assertTrue(
            "Password should be aleast 8 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="Aede",
                confirm_password="Aede",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Password should be aleast 8 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/register",
            data=dict(
                username="thrain",
                password="",
                confirm_password="",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter your password" in response.get_data(as_text=True))

    def test_get_pets(self):
        """Test GET /pets"""
        # No pets
        response = self.client.get("/pets")
        self.assertEqual(response.status_code, 200)
        expected_data = (
            "<!doctype html>\n<title>PetsRUs</title>\n\n    No pets found.\n"
        )
        self.assertEqual(expected_data, response.get_data(as_text=True))

        # Add pets and test
        maxx = Pet(
            name="Max",
            date_of_birth=date(2001, 1, 1),
            species="canine",
            breed="Jack Russell Terrier",
            sex="m",
            colour_and_identifying_marks="White with tan markings",
        )
        self.session.add(maxx)
        duke = Pet(
            name="Duke",
            date_of_birth=date(2001, 1, 2),
            species="canine",
            breed="Newfoundland",
            sex="m",
            colour_and_identifying_marks="Black",
        )
        self.session.add(duke)
        self.session.commit()
        response = self.client.get("/pets")
        expected_data = "<!doctype html>\n<title>PetsRUs</title>\n\n<ul>\n    \n    <li> Name: Max Breed: Jack Russell Terrier Species: canine </li>\n    \n    <li> Name: Duke Breed: Newfoundland Species: canine </li>\n    \n</ul>\n"  # noqa
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_data, response.get_data(as_text=True))
        self.session.query(Pet).delete()
        self.session.commit()


if __name__ == "__main__":
    unittest.main()
