# coding=utf-8
import os
import unittest
import warnings
from datetime import date, timedelta
from io import BytesIO

from petsrus.models.models import Pet, Schedule, ScheduleType, User
from petsrus.petsrus import app
from petsrus.tests.helper import (add_pet_helper, add_pet_schedule_helper,
                                  login_user_helper, random_pet,
                                  random_schedule, register_user_helper)
from petsrus.views.main import db_session


class TestCasePets(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session
        self.db_session.query(Schedule).delete()
        self.db_session.query(ScheduleType).delete()
        self.db_session.query(Pet).delete()
        self.db_session.query(User).delete()
        self.db_session.commit()
        for schedule_type_name in ["Vaccine", "Deworming", "Frontline"]:
            schedule_type = ScheduleType(name=schedule_type_name)
            db_session.add(schedule_type)
        self.db_session.commit()

    def tearDown(self):
        self.db_session.query(Schedule).delete()
        self.db_session.query(ScheduleType).delete()
        self.db_session.query(Pet).delete()
        self.db_session.query(User).delete()
        self.db_session.commit()
        self.db_session.close()

    def test_validate_pet_details_on_edit(self):
        """Test valid pet details on edit /edit_pet/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        # Add pet
        pet = add_pet_helper(self.db_session, random_pet())

        # Edit Pet
        response = self.client.get("/edit_pet/{}".format(pet.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'value="{}"'.format(pet.name) in response.get_data(as_text=True)
        )
        self.assertTrue(
            'value="{}"'.format(pet.species) in response.get_data(as_text=True)
        )
        self.assertTrue(
            'value="{}"'.format(pet.breed) in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/edit_pet/{}".format(pet.id),
            data=dict(name="S", species="c", breed="r"),
            follow_redirects=True,
        )
        self.assertTrue(
            "Name must be between 2 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "Breed must be between 5 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "Species must be between 4 to 10 characters in length"
            in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_pets_validate_name(self):
        """Test pet name validation"""
        warnings.simplefilter("ignore", DeprecationWarning)
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="",
                date_of_birth="2019-01-01",
                species="canine",
                breed="Mastiff",
                sex="M",
                color_and_identifying_marks="Black with brown spots",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Please enter a name" in response.get_data(as_text=True))
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="I",
                date_of_birth="2019-01-01",
                species="canine",
                breed="Mastiff",
                sex="M",
                color_and_identifying_marks="Black with brown spots",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Name must be between 2 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="I have a really long name that can not be saved",
                date_of_birth="2019-01-01",
                species="canine",
                breed="Mastiff",
                sex="M",
                color_and_identifying_marks="Black with brown spots",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Name must be between 2 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

    def test_pets_validate_date_of_birth(self):
        """Test date of birth validation"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="",
                species="canine",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a Date of Birth (YYYY-MM-DD)"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                # Date format DD-MM-YYYY
                date_of_birth="23-04-2019",
                species="canine",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a Date of Birth (YYYY-MM-DD)"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                # Date in the future
                date_of_birth=date.today() + timedelta(days=2),
                species="canine",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a date before {}".format(date.today())
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

    def test_pets_validate_species(self):
        """Test species validation"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please provide species details" in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="can",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Species must be between 4 to 10 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="This is a really long name for a species",
                breed="German Shepherd",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Species must be between 4 to 10 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

    def test_pets_validate_breed(self):
        """Test breed validation"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="canine",
                breed="",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please provide breed details" in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="canine",
                breed="G",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Breed must be between 5 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="canine",
                breed="This is a really long name for a dog breed",
                sex="M",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Breed must be between 5 to 25 characters in length"
            in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

    def test_pets_validate_sex(self):
        """Test sex validation"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="canine",
                breed="German Shepherd",
                sex="",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please provide pet sex details" in response.get_data(as_text=True)
        )
        self.assertEqual(0, self.db_session.query(Pet).count())

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Ace",
                date_of_birth="2001-01-01",
                species="canine",
                breed="G",
                sex="Male",
                color_and_identifying_marks="Black with brown patches",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue("Enter M or F for sex" in response.get_data(as_text=True))
        self.assertEqual(0, self.db_session.query(Pet).count())

    def test_get_pets(self):
        """Test GET / to view pets"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        # Add some pets
        first_pet = add_pet_helper(self.db_session, random_pet())
        second_pet = add_pet_helper(self.db_session, random_pet())

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ">{}</a>".format(first_pet.name) in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(first_pet.breed.title())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(first_pet.species.title())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            ">{}</a>".format(second_pet.name) in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(second_pet.breed.title())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(second_pet.species.title())
            in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_edit_pets(self):
        """Test GET, POST /edit_pet/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        pet = add_pet_helper(self.db_session, random_pet())

        # Edit Pet
        response = self.client.get("/edit_pet/{}".format(pet.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            'value="{}"'.format(pet.name) in response.get_data(as_text=True)
        )
        self.assertTrue(
            'value="{}"'.format(pet.species) in response.get_data(as_text=True)
        )
        self.assertTrue(
            'value="{}"'.format(pet.breed) in response.get_data(as_text=True)
        )

        response = self.client.post(
            "/edit_pet/{}".format(pet.id),
            data=dict(name="Sykes", species="canine", breed="russian grey", sex="m"),
            follow_redirects=True,
        )
        self.assertTrue(">Sykes</a>" in response.get_data(as_text=True))
        self.assertTrue("<td>Canine</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Russian Grey</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_delete_pets(self):
        """Test POST /delete_pet/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        pet = add_pet_helper(self.db_session, random_pet())

        # Delete Pet
        response = self.client.post(
            "/delete_pet/{}".format(pet.id), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_delete_pets_with_schedules(self):
        """Test POST /delete_pet/<int:pet_id> with schedules"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        add_pet_schedule_helper(self.db_session, pet, random_schedule(self.db_session))
        add_pet_schedule_helper(self.db_session, pet, random_schedule(self.db_session))

        self.assertEqual(2, self.db_session.query(Schedule).count())

        # Delete Pet
        response = self.client.post(
            "/delete_pet/{}".format(pet.id), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_pets(self):
        """Test POST /add_pet"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        response = self.client.post(
            "/add_pet",
            data=dict(
                name="Lewis",
                date_of_birth="2019-01-01",
                species="canine",
                breed="Mastiff",
                sex="M",
                color_and_identifying_marks="Black with brown spots",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, self.db_session.query(Pet).count())

    def test_view_pet_details(self):
        """Test GET /view_pet"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())

        response = self.client.get("/view_pet/{}".format(pet.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            ">{}</td>".format(pet.name.title()) in response.get_data(as_text=True)
        )
        self.assertTrue(
            ">{}</td>".format(pet.date_of_birth) in response.get_data(as_text=True)
        )
        self.assertTrue(
            ">{}</td>".format(pet.breed.title()) in response.get_data(as_text=True)
        )
        self.assertTrue(
            ">{}</td>".format(pet.sex.title()) in response.get_data(as_text=True)
        )
        self.assertTrue(
            ">{}</td>".format(pet.colour_and_identifying_marks)
            in response.get_data(as_text=True)
        )

        # Attempting to view unknown pets should return a 404
        response = self.client.get("/view_pet/{}".format(0))
        self.assertEqual(response.status_code, 404)
        self.assertTrue(
            "h5>{}</h5".format("Sorry, Pet does not exist.")
            in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_validate_pet_schedule_details(self):
        """Test valid details on creating a schedule /add_schedule/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        vaccine = (
            db_session.query(ScheduleType)
            .filter(ScheduleType.name == "Vaccine")
            .first()
        )

        # Add Pet Schedule - No data entered
        response = self.client.post(
            "/add_schedule/{}".format(pet.id),
            data=dict(
                schedule_type=vaccine.id, date_of_next="", repeats="", repeat_cycle="",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter the Date (YYYY-MM-DD)" in response.get_data(as_text=True)
        )
        self.assertTrue(
            "Please select either Yes or No" in response.get_data(as_text=True)
        )

        # Add schedule, with a date in the past
        response = self.client.post(
            "/add_schedule/{}".format(pet.id),
            data=dict(
                schedule_type=vaccine.id,
                date_of_next="2001-02-01",
                repeats="",
                repeat_cycle="",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            "Please enter a date greater than today {}".format(date.today())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "Please select either Yes or No" in response.get_data(as_text=True)
        )

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_new_pet_schedule(self):
        """Test POST /add_schedule/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        vaccine = (
            db_session.query(ScheduleType)
            .filter(ScheduleType.name == "Vaccine")
            .first()
        )
        response = self.client.post(
            "/add_schedule/{}".format(pet.id),
            data=dict(
                schedule_type=vaccine.id,
                date_of_next=date.today() + timedelta(days=1),
                repeats="YES",
                repeat_cycle="YEARLY",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, self.db_session.query(Schedule).count())

    def test_add_new_pet_schedule_no_repeat_cycle(self):
        """Test POST /add_schedule/<int:pet_id> without a repeat_cycle"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        frontline = (
            db_session.query(ScheduleType)
            .filter(ScheduleType.name == "Frontline")
            .first()
        )

        response = self.client.post(
            "/add_schedule/{}".format(pet.id),
            data=dict(
                schedule_type=frontline.id,
                date_of_next=date.today() + timedelta(days=2),
                repeats="NO",
                repeat_cycle=None,
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, self.db_session.query(Schedule).count())

    def test_view_pet_schedules(self):
        """Test GET /view_pet with due and past schedules"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        due_schedule = add_pet_schedule_helper(
            self.db_session, pet, random_schedule(self.db_session)
        )
        past_schedule = add_pet_schedule_helper(
            self.db_session, pet, random_schedule(self.db_session, past=True)
        )

        self.assertEqual(2, self.db_session.query(Schedule).count())

        response = self.client.get("/view_pet/{}".format(pet.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(">{}</td>".format(pet.name) in response.get_data(as_text=True))
        self.assertTrue("<h5>Schedules</h5>" in response.get_data(as_text=True))
        self.assertTrue(
            "<td>{}</td>".format(due_schedule.schedule_types.name.title())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(due_schedule.date_of_next)
            in response.get_data(as_text=True)
        )
        self.assertTrue("<h5>History</h5>" in response.get_data(as_text=True))
        self.assertTrue(
            "<td>{}</td>".format(past_schedule.schedule_types.name.title())
            in response.get_data(as_text=True)
        )
        self.assertTrue(
            "<td>{}</td>".format(past_schedule.date_of_next)
            in response.get_data(as_text=True)
        )

    def test_delete_pet_schedule(self):
        """Test POST /delete_schedule"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        pet_schedule = add_pet_schedule_helper(
            self.db_session, pet, random_schedule(self.db_session)
        )

        self.assertEqual(1, self.db_session.query(Schedule).count())

        response = self.client.post(
            "/delete_schedule/{}".format(pet_schedule.id), follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(0, self.db_session.query(Schedule).count())

    def test_update_pet_photo_validation(self):
        """Test validation for updating a pet photo"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        response = self.client.post(
            "/update_pet_photo/{}".format(pet.id),
            data={"image_file": (BytesIO("IMAGE DATA".encode()), "picture.jpg")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(
            "No file part", response.get_data(as_text=True),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/update_pet_photo/{}".format(pet.id),
            data={"photo": (BytesIO("IMAGE DATA".encode()), "")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(
            "No selected photo", response.get_data(as_text=True),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/update_pet_photo/{}".format(pet.id),
            data={"photo": (BytesIO("IMAGE DATA".encode()), "picture.wrong_extension")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(
            "Photo type not allowed. Use png, gif, jpeg or jpg",
            response.get_data(as_text=True),
        )
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/update_pet_photo/{}".format(pet.id),
            data={"photo": (BytesIO("IMAGE DATA".encode()), "picture.jpg")},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(
            "Unidentified Image Error", response.get_data(as_text=True),
        )
        self.assertEqual(response.status_code, 200)

    def test_update_pet_photo(self):
        """Test updating a pet photo"""
        # https://github.com/boto/boto3/issues/454
        # https://github.com/psf/requests/issues/3912
        warnings.simplefilter("ignore", ResourceWarning)
        register_user_helper(self.client)
        login_user_helper(self.client)

        pet = add_pet_helper(self.db_session, random_pet())
        test_image = os.path.join("./petsrus/tests/assets/2020155847.jpg")
        response = self.client.post(
            "/update_pet_photo/{}".format(pet.id),
            data={"photo": (test_image, "new_image.png",)},
            content_type="multipart/form-data",
            follow_redirects=True,
        )
        self.assertIn(
            "Changed Pet Photo", response.get_data(as_text=True),
        )
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
