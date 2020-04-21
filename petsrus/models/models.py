from enum import Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String


Base = declarative_base()


class classproperty:
    def __init__(self, func):
        self._func = func

    def __get__(self, obj, owner):
        return self._func(owner)


class Repeat_cycle(Enum):
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    YEARLY = "Yearly"

    @classproperty
    def __values__(cls):
        return [(repeat_cycle.name, repeat_cycle.value) for repeat_cycle in cls]


class Repeat(Enum):
    YES = "Yes"
    NO = "No"

    @classproperty
    def __values__(cls):
        return [(repeat.name, repeat.value) for repeat in cls]


class Schedule_type(Enum):
    VACCINE = "Vaccine"
    DEWORMING = "Deworming"
    FRONTLINE = "Frontline"

    # http://xion.io/post/code/python-enums-are-ok.html
    @classproperty
    def __values__(cls):
        return [(schedule_type.name, schedule_type.value) for schedule_type in cls]


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(32), unique=True, index=True)
    password = Column(String(128), nullable=False)
    email_address = Column(String(50), unique=True, index=True)
    telephone = Column(String(20), nullable=True)
    country = Column(String(50), nullable=True)
    authenticated = Column(Boolean, default=False)

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        return "<User {}>".format(self.username)


class Pet(Base):
    __tablename__ = "pets"
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    date_of_birth = Column(Date(), nullable=False)
    species = Column(String(10), nullable=False)
    breed = Column(String(20), nullable=False)
    sex = Column(String(1), nullable=False)
    colour_and_identifying_marks = Column(String(200), nullable=False)

    def __repr__(self):
        return (
            "<Pet name: {}\ndate_of_birth: {}\nspecies: {}\nbreed: {}\n"
            "sex: {}\ncolour_and_identifying_marks: {}\n>"
        ).format(
            self.name,
            self.date_of_birth,
            self.species,
            self.breed,
            self.sex,
            self.colour_and_identifying_marks,
        )


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    date_of_next = Column(Date(), nullable=False)
    repeats = Column(String(3), nullable=False)
    repeat_cycle = Column(String(10), nullable=False)
    schedule_type = Column(String(10), nullable=False)

    def __repr__(self):
        return (
            "<Schedule pet_id: {}\ndate_of_next: {}\nrepeats: {}\n"
            "repeat_cycle: {}\nschedule_type: {}\n>"
        ).format(
            self.pet_id,
            self.date_of_next,
            self.repeats,
            self.repeat_cycle,
            self.schedule_type,
        )
