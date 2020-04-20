# coding=utf-8
import unittest

from datetime import date

from petsrus.petsrus import app
from petsrus.models.models import Pet, Schedule, User
from petsrus.views.main import db_session
from petsrus.tests.helper import register_user_helper, login_user_helper


class TestCasePets(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session

    def tearDown(self):
        self.db_session.query(Schedule).delete()
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
        duke = Pet(
            name="duchess",
            date_of_birth=date(2001, 1, 2),
            species="feline",
            breed="russian blue",
            sex="m",
            colour_and_identifying_marks="b",
        )
        self.db_session.add(duke)
        self.db_session.commit()

        # Edit Pet
        response = self.client.get("/edit_pet/{}".format(duke.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('value="duchess"' in response.get_data(as_text=True))
        self.assertTrue('value="feline"' in response.get_data(as_text=True))
        self.assertTrue('value="russian blue"' in response.get_data(as_text=True))

        response = self.client.post(
            "/edit_pet/{}".format(duke.id),
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

        self.db_session.query(Pet).delete()
        self.db_session.commit()

    def test_pets_validate_name(self):
        """Test pet name validation"""
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

        # Add pets and test
        maxx = Pet(
            name="maxx",
            date_of_birth=date(2001, 1, 1),
            species="canine",
            breed="jack russell terrier",
            sex="m",
            colour_and_identifying_marks="White with tan markings",
        )
        self.db_session.add(maxx)
        duke = Pet(
            name="duchess",
            date_of_birth=date(2001, 1, 2),
            species="feline",
            breed="russian blue",
            sex="m",
            colour_and_identifying_marks="Black",
        )
        self.db_session.add(duke)
        self.db_session.commit()
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(">Maxx</a>" in response.get_data(as_text=True))
        self.assertTrue(
            "<td>Jack Russell Terrier</td>" in response.get_data(as_text=True)
        )
        self.assertTrue("<td>Canine</td>" in response.get_data(as_text=True))
        self.assertTrue(">Duchess</a>" in response.get_data(as_text=True))
        self.assertTrue("<td>Feline</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Russian Blue</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

        self.db_session.query(Pet).delete()
        self.db_session.commit()

    def test_edit_pets(self):
        """Test GET, POST /edit_pet/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        # Add pet
        duke = Pet(
            name="duchess",
            date_of_birth=date(2001, 1, 2),
            species="feline",
            breed="russian blue",
            sex="m",
            colour_and_identifying_marks="Black",
        )
        self.db_session.add(duke)
        self.db_session.commit()

        # Edit Pet
        response = self.client.get("/edit_pet/{}".format(duke.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('value="duchess"' in response.get_data(as_text=True))
        self.assertTrue('value="feline"' in response.get_data(as_text=True))
        self.assertTrue('value="russian blue"' in response.get_data(as_text=True))

        response = self.client.post(
            "/edit_pet/{}".format(duke.id),
            data=dict(name="Sykes", species="canine", breed="russian grey"),
            follow_redirects=True,
        )
        self.assertTrue(">Sykes</a>" in response.get_data(as_text=True))
        self.assertTrue("<td>Canine</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Russian Grey</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

        self.db_session.query(Pet).delete()
        self.db_session.commit()

    def test_delete_pets(self):
        """Test POST /delete_pet/<int:pet_id>"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        # Add pet
        duke = Pet(
            name="duchess",
            date_of_birth=date(2001, 1, 2),
            species="feline",
            breed="russian blue",
            sex="m",
            colour_and_identifying_marks="Black",
        )
        self.db_session.add(duke)
        self.db_session.commit()

        # Delete Pet
        response = self.client.post(
            "/delete_pet/{}".format(duke.id), follow_redirects=True
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

        # Add pet
        gin = Pet(
            name="Gin",
            date_of_birth=date(2001, 11, 22),
            species="feline",
            breed="collie",
            sex="m",
            colour_and_identifying_marks="Black",
        )

        self.db_session.add(gin)
        self.db_session.commit()

        response = self.client.get("/view_pet/{}".format(gin.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(">Gin</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>2001-11-22</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>collie</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>m</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Black</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_add_new_pet_schedule(self):
        """Test POST /add_schedule"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # Add pet
        kira = Pet(
            name="Kira",
            date_of_birth=date(2001, 11, 22),
            species="feline",
            breed="corgi",
            sex="f",
            colour_and_identifying_marks="white puppy with black ears",
        )

        self.db_session.add(kira)
        self.db_session.commit()

        response = self.client.post(
            "/add_schedule/{}".format(kira.id),
            data=dict(
                schedule_type="VACCINE",
                date_of_next="2019-02-15",
                repeats="YES",
                repeat_cycle="YEARLY",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, self.db_session.query(Schedule).count())

    def test_add_new_pet_schedule_no_repeat_cycle(self):
        """Test POST /add_schedule without a repeat_cycle"""
        register_user_helper(self.client)
        login_user_helper(self.client)

        # Add pet
        gin = Pet(
            name="Gin",
            date_of_birth=date(2001, 11, 22),
            species="reptile",
            breed="guppy",
            sex="f",
            colour_and_identifying_marks="silver and really tiny",
        )

        self.db_session.add(gin)
        self.db_session.commit()

        response = self.client.post(
            "/add_schedule/{}".format(gin.id),
            data=dict(
                schedule_type="FRONTLINE",
                date_of_next="2019-02-15",
                repeats="NO",
                repeat_cycle="",
            ),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, self.db_session.query(Schedule).count())


if __name__ == "__main__":
    unittest.main()
