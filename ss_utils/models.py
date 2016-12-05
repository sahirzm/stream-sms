from django.db import models
from enum import Enum, unique, IntEnum

@unique
class FilterOperator(Enum):
    EQUAL = 'EQUAL'
    NOT_EQUAL = 'NOT_EQUAL'
    CONTAIN = 'CONTAIN'
    DOES_NOT_CONTAIN = 'DOES_NOT_CONTAIN'
    STARTS_WITH = 'STARTS_WITH'
    ENDS_WITH = 'ENDS_WITH'
    GREATER_THAN = 'GREATER_THAN'
    LESS_THAN = 'LESS_THAN'
    GREATER_THAN_EQUAL = 'GREATER_THAN_EQUAL'
    LESS_THAN_EQUAL = 'LESS_THAN_EQUAL'
    BETWEEN = 'BETWEEN'
    IN = 'IN'
    NOT_IN = 'NOT_IN'
    IS_EMPTY = 'IS_EMPTY'
    IS_NOT_EMPTY = 'IS_NOT_EMPTY'

    @staticmethod
    def from_str(oper):
        for o in FilterOperator:
            if o.value == oper:
                return o
        raise ValueError("{} is not supported filter operator".format(oper))

@unique
class FieldType(IntEnum):
    Number = 1
    Date = 2
    String = 3

class Filter(object):

    def __init__(self, field, value, operator):
        self.field = field
        self.value = value
        self.operator = operator

    def get_num_vals(self):
        return [float(num) if "." in num else int(num) for num in self.value.split(",")]

    def get_vals(self):
        return [val.strip() for val in self.value.split(",")]

    def get_val(self):
        return self.value

    def get_num(self):
        return float(self.value) if "." in self.value else int(self.value)

    def get_date(self):
        return self.value

    def get_dates(self):
        return self.value

    def get_is_empty(self):
        return True

    def get_is_not_empty(self):
        return False
