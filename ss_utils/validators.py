from django.core.exceptions import ValidationError
from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator

@deconstructible
class NameValidator(RegexValidator):

    def __init__(self, code=None, space=False, message=None):
        if message is None:
            if space:
                message = 'Can contain chars and space.'
            else:
                message = 'Can contain chars only'

        if space:
            regex = r"^[a-zA-Z]*\s*[a-zA-Z]*$"
        else:
            regex = r"^[a-zA-Z]$"

        # calling the super class init
        super().__init__(regex, message, code)


@deconstructible
class PhoneValidator(RegexValidator):

    def __init__(self, code=None, message=None):
        if message is None:
            message = 'Invalid phone number.'

        regex = r"^(\+?1-?)?(([2-9]\d{2})|[2-9]\d{2})-?[2-9]\d{2}-?\d{4}$"

        # calling the super class init
        super().__init__(regex, message, code)


@deconstructible
class SSNValidator(RegexValidator):

    def __init__(self, code=None, message=None):
        if message is None:
            message = 'Invalid SSN'

        regex = r"^\d{3}-\d{2}-\d{4}$"

        #calling the super class init
        super().__init__(regex, message, code)


@deconstructible
class SizeValidator(object):

    def __init__(self, min, max, code=None, message=None):
        if message is None:
            if min == max:
                message = 'length must be %(min)s'
            else:
                message = 'length must be between %(min)s and %(max)s'

        if code is None:
            code = 'size_validate'

        self.min = min
        self.max = max
        self.code = code
        self.message = message

    def __call__(self, value):
        cleaned = self.clean(value)
        params = {'min': self.min, 'max': self.max}
        if (len(cleaned) < self.min or len(cleaned) > self.max):
            raise ValidationError(self.message, code=self.code, params=params)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and (self.min == other.min
                ) and (self.max == other.max) and (self.message == other.message
                        ) and (self.code == other.code)

    def clean(self, value):
        return value.strip() if value else ""
