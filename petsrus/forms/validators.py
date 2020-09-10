from datetime import date

from petsrus.models.models import RepeatCycle
from petsrus.views.main import db_session
from sqlalchemy import func
from wtforms.validators import ValidationError


class PastDate(object):
    def __init__(self, message=None):
        if not message:
            message = u"Only use today ({}) or earlier dates earlier".format(
                date.today()
            )
        self.message = message

    def __call__(self, form, field):
        if field.data > date.today():
            raise ValidationError(self.message)


class FutureDate(object):
    def __init__(self, message=None):
        if not message:
            message = u"Only dates after today ({}) are allowed".format(date.today())
        self.message = message

    def __call__(self, form, field):
        if field.data <= date.today():
            raise ValidationError(self.message)


class ExistingRepeatCycle(object):
    def __init__(self, message=None):
        if not message:
            message = u"This Repeat Cycle already exists"
        self.message = message

    def __call__(self, form, field):
        repeat_cycles = (
            db_session.query(RepeatCycle)
            .filter(func.lower(RepeatCycle.name) == func.lower(field.data))
            .all()
        )
        if repeat_cycles:
            raise ValidationError(self.message)
