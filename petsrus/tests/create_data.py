# https://topdogtips.com/most-awesome-dogs-in-anime/
# For the pictures
# http://www.puppiesndogs.com/breeds
# https://wamiz.co.uk/cat/breeds
import os
import random

from werkzeug.security import generate_password_hash

from petsrus.models.models import Pet, Schedule, User
from petsrus.tests.helper import (add_pet_helper, add_pet_schedule_helper,
                                  random_pet, random_schedule)
from petsrus.views.main import db_session

# Drop previous data
db_session.query(Schedule).delete()
db_session.query(Pet).delete()
db_session.query(User).delete()


user = User(
    username=os.environ.get("TEST_USERNAME"),
    password=generate_password_hash(os.environ.get("TEST_PASSWORD")),
    email_address=os.environ.get("EMAIL_ADDRESS"),
)

db_session.add(user)
db_session.commit()

for _ in range(5):
    pet = add_pet_helper(db_session, random_pet())
    for _ in range(random.randint(1, 3)):
        due_schedule = add_pet_schedule_helper(db_session, pet, random_schedule())
    for _ in range(random.randint(1, 5)):
        past_schedule = add_pet_schedule_helper(
            db_session, pet, random_schedule(past=True)
        )
