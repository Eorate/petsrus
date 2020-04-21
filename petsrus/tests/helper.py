# coding=utf-8
from petsrus.models.models import Pet


def register_user_helper(client):
    """Helper function to register user"""
    return client.post(
        "/register",
        data=dict(
            username="Ebodius",
            password="Crimsaurus",
            confirm_password="Crimsaurus",
            email_address="ebodius@example.com",
        ),
        follow_redirects=True,
    )


def login_user_helper(client):
    """Helper function to login user"""
    return client.post(
        "/", data=dict(username="Ebodius", password="Crimsaurus"), follow_redirects=True
    )


def add_pet_helper(db_session, pet):
    """Helper function to add a pet"""
    pet = Pet(
        name=pet["name"],
        date_of_birth=pet["date"],
        species=pet["species"],
        breed=pet["breed"],
        sex=pet["sex"],
        colour_and_identifying_marks=pet["description"],
    )
    db_session.add(pet)
    db_session.commit()

    return pet
