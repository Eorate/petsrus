from enum import Enum

from sqlalchemy import Boolean, Column, Date, ForeignKey, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class classproperty:
    def __init__(self, func):
        self._func = func

    def __get__(self, obj, owner):
        return self._func(owner)


class Repeat(Enum):
    YES = "Yes"
    NO = "No"

    # http://xion.io/post/code/python-enums-are-ok.html
    @classproperty
    def __values__(cls):
        return [(repeat.name, repeat.value) for repeat in cls]


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
    photo = Column(Text, nullable=True, default="default.png")

    schedules = relationship(
        "Schedule", backref="pet", cascade="all, delete, delete-orphan"
    )

    def __repr__(self):
        return (
            "<Pet\nid: {}\nname: {}\ndate_of_birth: {}\nspecies: {}\nbreed: {}\n"
            "sex: {}\ncolour_and_identifying_marks: {}\nphoto: {}\n>"
        ).format(
            self.id,
            self.name,
            self.date_of_birth,
            self.species,
            self.breed,
            self.sex,
            self.colour_and_identifying_marks,
            self.photo,
        )


class Schedule(Base):
    __tablename__ = "schedules"
    id = Column(Integer, primary_key=True)
    pet_id = Column(Integer, ForeignKey("pets.id"), nullable=False)
    date_of_next = Column(Date(), nullable=False)
    repeats = Column(String(3), nullable=False)
    repeat_cycle = Column(Integer, ForeignKey("repeat_cycles.id"), nullable=True)
    schedule_type = Column(Integer, ForeignKey("schedule_types.id"), nullable=True)

    schedule_types = relationship("ScheduleType", backref="schedule_types")
    repeat_cycles = relationship("RepeatCycle", backref="repeat_cycles")

    def __repr__(self):
        return (
            "<Schedule\nid: {}\npet_id: {}\ndate_of_next: {}\nrepeats: {}\n"
            "repeat_cycle: {}\nschedule_type_id:{}\nschedule_type_name: {}\n>"
        ).format(
            self.id,
            self.pet_id,
            self.date_of_next,
            self.repeats,
            self.repeat_cycles.id,
            self.repeat_cycles.name,
            self.schedule_types.id,
            self.schedule_types.name,
        )


class ScheduleType(Base):
    __tablename__ = "schedule_types"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return ("<ScheduleType\nid: {}\nschedule_type: {}\n>").format(
            self.id, self.name,
        )


class RepeatCycle(Base):
    __tablename__ = "repeat_cycles"
    id = Column(Integer, primary_key=True)
    name = Column(String(20), nullable=False)

    def __repr__(self):
        return ("<RepeatCycle\nid: {}\nrepeat_cycle: {}\n>").format(self.id, self.name,)
