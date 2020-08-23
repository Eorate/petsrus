# https://topdogtips.com/most-awesome-dogs-in-anime/
# For the pictures
# http://www.puppiesndogs.com/breeds
# https://wamiz.co.uk/cat/breeds
import os
import random

from petsrus.models.models import Pet, RepeatCycle, Schedule, ScheduleType, User
from petsrus.tests.helper import (
    add_pet_helper,
    add_pet_schedule_helper,
    random_pet,
    random_schedule,
)
from petsrus.views.main import db_session
from werkzeug.security import generate_password_hash

# Drop previous data
db_session.query(Schedule).delete()
db_session.query(ScheduleType).delete()
db_session.query(RepeatCycle).delete()
db_session.query(Pet).delete()
db_session.query(User).delete()


user = User(
    username=os.environ.get("TEST_USERNAME"),
    password=generate_password_hash(os.environ.get("TEST_PASSWORD")),
    email_address=os.environ.get("EMAIL_ADDRESS"),
)

db_session.add(user)

for schedule_type_name in ["Vaccine", "Deworming", "Frontline"]:
    schedule_type = ScheduleType(name=schedule_type_name)
    db_session.add(schedule_type)

for repeat_cycle_name in ["Monthly", "Quarterly", "Yearly"]:
    repeat_cycle = RepeatCycle(name=repeat_cycle_name)
    db_session.add(repeat_cycle)

db_session.commit()

for _ in range(5):
    pet = add_pet_helper(db_session, random_pet())
    for _ in range(random.randint(1, 3)):
        due_schedule = add_pet_schedule_helper(
            db_session, pet, random_schedule(db_session)
        )
    for _ in range(random.randint(1, 5)):
        past_schedule = add_pet_schedule_helper(
            db_session, pet, random_schedule(db_session, past=True)
        )
