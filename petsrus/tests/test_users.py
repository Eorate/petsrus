# coding=utf-8
import logging
import unittest

from petsrus.models.models import User
from petsrus.petsrus import app
from petsrus.tests.helper import login_user_helper, register_user_helper
from petsrus.views.main import db_session


class TestCaseUsers(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session
        self.db_session.query(User).delete()
        self.db_session.commit()

    def tearDown(self):
        self.db_session.query(User).delete()
        self.db_session.commit()
        self.db_session.close()

    def test_index(self):
        """Test GET /"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Test login POST /"""
        response = register_user_helper(self.client)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/",
            data=dict(username="Ebodius", password="Crimsaurus"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username_or_password(self):
        """Test login POST / fails if wrong username or password"""
        response = register_user_helper(self.client)
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/", data=dict(username="thrain", password="thrain")
        )
        self.assertEqual(response.status_code, 200)

        self.assertTrue(
            "Sorry, username or password was incorrect"
            in response.get_data(as_text=True)
        )

    def test_logout(self):
        """Test GET /logout"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/add_pet")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        """Test POST /register"""
        response = register_user_helper(self.client)
        self.assertEqual(response.status_code, 200)

        self.assertTrue("Login" in response.get_data(as_text=True))
        self.assertTrue("Thanks for registering" in response.get_data(as_text=True))
        self.assertEqual(1, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

    def test_register_duplicate_username(self):
        """Test duplicate username validation"""
        response = self.client.post(
            "/register",
            data=dict(
                username="Aedel",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Thanks for registering" in response.get_data(as_text=True))
        self.assertEqual(1, self.db_session.query(User).count())

        response = self.client.post(
            "/register",
            data=dict(
                username="Aedel",
                password="Aedelwulf",
                confirm_password="Aedelwulf",
                email_address="thrain@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (
                "Sorry, Username &#39;Aedel&#39; or Email "
                "&#39;thrain@example.com&#39; is already in use"
            )
            in response.get_data(as_text=True)
        )
        self.assertEqual(1, self.db_session.query(User).count())

    def test_register_duplicate_email_address(self):
        """Test duplicate email_address validation"""
        response = self.client.post(
            "/register",
            data=dict(
                username="Euronotus",
                password="notuseuro",
                confirm_password="notuseuro",
                email_address="euronotus@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Thanks for registering" in response.get_data(as_text=True))
        self.assertEqual(1, self.db_session.query(User).count())

        response = self.client.post(
            "/register",
            data=dict(
                username="Euronotus",
                password="notuseuro",
                confirm_password="notuseuro",
                email_address="euronotus@example.com",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            (
                "Sorry, Username &#39;Euronotus&#39; or Email "
                "&#39;euronotus@example.com&#39; is already in use"
            )
            in response.get_data(as_text=True)
        )
        self.assertEqual(1, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())

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
        self.assertEqual(0, self.db_session.query(User).count())


if __name__ == "__main__":
    unittest.main()
