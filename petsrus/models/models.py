from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import deferred
from sqlalchemy import Boolean, Column, Integer, String, Date, LargeBinary


Base = declarative_base()


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
        return "<Pet {}>".format(
            self.name,
            self.date_of_birth,
            self.species,
            self.breed,
            self.sex,
            self.colour_and_identifying_marks,
        )
