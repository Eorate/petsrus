from datetime import date

from sqlalchemy import func
from wtforms.validators import ValidationError

from petsrus.models.models import RepeatCycle
from petsrus.views.main import db_session


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


class ExistingName(object):
    def __init__(self, table_name, message=None):
        if not message:
            message = u"This name already exists"
        self.message = message
        self.table_name = table_name

    def __call__(self, form, field):
        names = (
            db_session.query(self.table_name)
            .filter(func.lower(self.table_name.name) == func.lower(field.data))
            .all()
        )
        if names:
            raise ValidationError(self.message)
