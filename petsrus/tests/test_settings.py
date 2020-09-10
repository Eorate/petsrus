# coding=utf-8
import unittest

from sqlalchemy import func

from petsrus.models.models import RepeatCycle, ScheduleType, User
from petsrus.petsrus import app
from petsrus.tests.helper import login_user_helper, register_user_helper
from petsrus.views.main import db_session


class TestCaseSettings(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session
        self.db_session.query(User).delete()
        self.db_session.query(RepeatCycle).delete()
        self.db_session.query(ScheduleType).delete()
        self.db_session.commit()

    def tearDown(self):
        self.db_session.query(User).delete()
        self.db_session.query(RepeatCycle).delete()
        self.db_session.query(ScheduleType).delete()
        self.db_session.commit()
        self.db_session.close()

    def test_validate_settings_repeat_cycle(self):
        """Test valid repeat cycle details on add /settings/account_details/repeat_cycles"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/settings/account_details/repeat_cycles")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Add Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details/repeat_cycles",
            data=dict(repeat_cycle_name=""),
            follow_redirects=True,
        )
        self.assertTrue(
            "Please provide a Repeat Cycle eg Daily, Weekly etc"
            in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/settings/account_details/repeat_cycles",
            data=dict(repeat_cycle_name="S"),
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
            "/settings/account_details/repeat_cycles",
            data=dict(repeat_cycle_name="weeKLY"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details/repeat_cycles",
            data=dict(repeat_cycle_name="WEEkly"),
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
            "/settings/account_details/repeat_cycles",
            data=dict(repeat_cycle_name="Daily"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Repeat Cycle" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_validate_settings_schedule_type(self):
        """Test valid schedule type details on add /settings/account_details/schedule_types"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/settings/account_details/schedule_types")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Add Schedule Type" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details/schedule_types",
            data=dict(schedule_type_name=""),
            follow_redirects=True,
        )
        self.assertTrue(
            "Please provide a Schedule Type eg Deworming, Vaccine etc"
            in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/settings/account_details/schedule_types",
            data=dict(schedule_type_name="G"),
            follow_redirects=True,
        )
        self.assertTrue(
            "Name must be between 5 to 20 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_duplicate_schedule_type(self):
        """Test add duplicate schedule type details """
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/settings/account_details/schedule_types",
            data=dict(schedule_type_name="grooMING"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Schedule Type" in response.get_data(as_text=True))

        response = self.client.post(
            "/settings/account_details/schedule_types",
            data=dict(schedule_type_name="GrOOminG"),
            follow_redirects=True,
        )
        self.assertTrue(
            "Sorry, this Schedule Type already exists"
            in response.get_data(as_text=True)
        )

        schedule_types = (
            db_session.query(ScheduleType)
            .filter(func.lower(ScheduleType.name) == func.lower("GROOMING"))
            .all()
        )

        self.assertEqual(len(schedule_types), 1)

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_schedule_type(self):
        """Test add schedule type details """
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/settings/account_details/schedule_types",
            data=dict(schedule_type_name="Grooming"),
            follow_redirects=True,
        )
        self.assertTrue("Saved Schedule Type" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)


if __name__ == "__main__":
    unittest.main()
