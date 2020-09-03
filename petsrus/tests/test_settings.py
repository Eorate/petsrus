# coding=utf-8
import unittest

from petsrus.models.models import RepeatCycle, User
from petsrus.petsrus import app
from petsrus.tests.helper import login_user_helper, register_user_helper
from petsrus.views.main import db_session
from sqlalchemy import func


class TestCaseSettings(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session
        self.db_session.query(User).delete()
        self.db_session.query(RepeatCycle).delete()
        self.db_session.commit()

    def tearDown(self):
        self.db_session.query(User).delete()
        self.db_session.query(RepeatCycle).delete()
        self.db_session.commit()
        self.db_session.close()

    def test_validate_settings_repeat_cycle(self):
        """Test valid repeat cycle details on add /settings/account_details"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/settings/account_details")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Add Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details",
            data=dict(name="S"),
            follow_redirects=True,
        )
        self.assertTrue(
            "Name must be between 5 to 20 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_duplicate_repeat_cycle(self):
        """Test add duplicate repeat cycle details """
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/settings/account_details",
            data=dict(name="weeKLY"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details",
            data=dict(name="WEEkly"),
            follow_redirects=True,
        )
        self.assertTrue(
            "Sorry, this Repeat Cycle already exists" in response.get_data(as_text=True)
        )

        repeat_cycles = (
            db_session.query(RepeatCycle)
            .filter(func.lower(RepeatCycle.name) == func.lower("WEEKLY"))
            .all()
        )

        self.assertEqual(len(repeat_cycles), 1)

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_repeat_cycle(self):
        """Test add repeat cycle details """
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/settings/account_details",
            data=dict(name="Daily"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
