# coding=utf-8
import unittest

from datetime import date

from petsrus.petsrus import app
from petsrus.models.models import Pet, User
from petsrus.views.main import db_session


class PetsRUsTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        self.client.testing = True
        self.db_session = db_session

    def tearDown(self):
        self.db_session.query(User).delete()
        self.db_session.query(Pet).delete()
        self.db_session.commit()
        self.db_session.close()

    def register_user_helper(self):
        """Helper function to register user"""
        return self.client.post(
            "/register",
            data=dict(
                username="Ebodius",
                password="Crimsaurus",
                confirm_password="Crimsaurus",
                email_address="ebodius@example.com",
            ),
            follow_redirects=True,
        )

    def login_user_helper(self):
        """Helper function to login user"""
        return self.client.post(
            "/",
            data=dict(username="Ebodius", password="Crimsaurus"),
            follow_redirects=True,
        )

    def test_index(self):
        """Test GET /"""
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_login(self):
        """Test login POST /"""
        response = self.register_user_helper()
        self.assertEqual(response.status_code, 200)

        response = self.client.post(
            "/",
            data=dict(username="Ebodius", password="Crimsaurus"),
            follow_redirects=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_login_invalid_username_or_password(self):
        """Test login POST / fails if wrong username or password"""
        response = self.register_user_helper()
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
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.get("/pets")
        self.assertEqual(response.status_code, 200)

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_register_user(self):
        """Test POST /register"""
        response = self.register_user_helper()
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

    def test_get_pets(self):
        """Test GET /pets"""
        self.register_user_helper()
        self.login_user_helper()

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        # Add pets and test
        maxx = Pet(
            name="max",
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
        self.assertTrue("<td>Max</td>" in response.get_data(as_text=True))
        self.assertTrue(
            "<td>Jack Russell Terrier</td>" in response.get_data(as_text=True)
        )
        self.assertTrue("<td>Canine</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Duchess</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Feline</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Russian Blue</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

        self.db_session.query(Pet).delete()
        self.db_session.commit()

    def test_edit_pets(self):
        """Test GET, POST /pets/<int:pet_id>"""
        self.register_user_helper()
        self.login_user_helper()

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
        response = self.client.get("/pets/{}".format(duke.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('value="duchess"' in response.get_data(as_text=True))
        self.assertTrue('value="feline"' in response.get_data(as_text=True))
        self.assertTrue('value="russian blue"' in response.get_data(as_text=True))

        response = self.client.post(
            "/pets/{}".format(duke.id),
            data=dict(name="Sykes", species="canine", breed="russian grey"),
            follow_redirects=True,
        )
        self.assertTrue("<td>Sykes</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Canine</td>" in response.get_data(as_text=True))
        self.assertTrue("<td>Russian Grey</td>" in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

        self.db_session.query(Pet).delete()
        self.db_session.commit()

    def test_validate_pet_details_on_edit(self):
        """Test valid pet details on edit /pets/<int:pet_id>"""
        self.register_user_helper()
        self.login_user_helper()

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
        response = self.client.get("/pets/{}".format(duke.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('value="duchess"' in response.get_data(as_text=True))
        self.assertTrue('value="feline"' in response.get_data(as_text=True))
        self.assertTrue('value="russian blue"' in response.get_data(as_text=True))

        response = self.client.post(
            "/pets/{}".format(duke.id),
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

    def test_delete_pets(self):
        """Test delete /pets/<int:pet_id>"""
        self.register_user_helper()
        self.login_user_helper()

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
        response = self.client.get("/pets/{}".format(duke.id))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('value="duchess"' in response.get_data(as_text=True))
        self.assertTrue('value="feline"' in response.get_data(as_text=True))
        self.assertTrue('value="russian blue"' in response.get_data(as_text=True))

        response = self.client.post("/delete/{}".format(duke.id), follow_redirects=True)
        self.assertEqual(response.status_code, 200)

        # No pets
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("No pets found." in response.get_data(as_text=True))

        response = self.client.get("/logout")
        self.assertEqual(response.status_code, 302)

    def test_pets_validate_name(self):
        """Test pet name validation"""
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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
            "/pets",
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
            "/pets",
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
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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
            "/pets",
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
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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
            "/pets",
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
            "/pets",
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
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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
            "/pets",
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
            "/pets",
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
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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
            "/pets",
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

    def test_add_pets(self):
        """Test POST /pets"""
        self.register_user_helper()
        self.login_user_helper()

        response = self.client.post(
            "/pets",
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


if __name__ == "__main__":
    unittest.main()
