from datetime import date

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
