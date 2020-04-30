# coding=utf-8
import random

from faker import Faker

from petsrus.models.models import Pet, Schedule

fake = Faker()


def random_pet():
    """Create random pet details"""
    sex = "M" if random.randint(0, 1) == 0 else "F"
    name = fake.first_name_male() if sex == "M" else fake.first_name_female()
    date_of_birth = fake.date_of_birth(tzinfo=None, minimum_age=1, maximum_age=10)
    species = fake.random_choices(elements=("feline", "canine"), length=1)[0]
    if species == "canine":
        breed = fake.random_choices(
            elements=("Boerboel", "Terrier", "Akita", "Bulldog", "Beagle", "Mastiff"),
            length=1,
        )[0]
    elif species == "feline":
        breed = fake.random_choices(
            elements=(
                "Bobtail",
                "Shorthair",
                "Balinese",
                "Bengal",
                "Birman",
                "Persian",
            ),
            length=1,
        )[0]
    description = fake.random_choices(
        elements=(
            "Black",
            "White",
            "Grey",
            "Brown",
            "Black and White",
            "Brown and Black",
        ),
        length=1,
    )[0]
    return {
        "name": name,
        "date": date_of_birth,
        "species": species,
        "breed": breed,
        "sex": sex,
        "description": description,
    }


def random_schedule(past=False):
    """Create random pet schedules"""
    schedule_type = fake.random_choices(
        elements=("VACCINE", "DEWORMING", "FRONTLINE"), length=1
    )[0]
    repeats = "YES" if random.randint(0, 1) == 0 else "NO"
    if repeats == "YES":
        repeat_cycle = fake.random_choices(
            elements=("MONTHLY", "QUARTERLY", "YEARLY"), length=1
        )[0]
        if repeat_cycle == "YEARLY":
            schedule_type = "VACCINE"
    else:
        repeat_cycle = None
    # We want some historical schedules
    if past:
        date_of_next = fake.date_this_year(before_today=True, after_today=False)
    else:
        date_of_next = fake.date_this_year(before_today=False, after_today=True)

    return {
        "schedule_type": schedule_type,
        "repeats": repeats,
        "repeat_cycle": repeat_cycle,
        "date": date_of_next,
    }


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


def add_pet_schedule_helper(db_session, pet, schedule):
    """Helper function to add a schedule for a pet"""
    pet_schedule = Schedule(
        pet_id=pet.id,
        date_of_next=schedule["date"],
        repeats=schedule["repeats"],
        repeat_cycle=schedule["repeat_cycle"],
        schedule_type=schedule["schedule_type"],
    )
    db_session.add(pet_schedule)
    db_session.commit()

    return pet_schedule
