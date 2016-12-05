import inspect
import json
from enum import Enum
from django.core.management import call_command
from datetime import datetime

class ChoiceEnum(Enum):

    @classmethod
    def choices(cls):
        # get all members of the class
        members = inspect.getmembers(cls, lambda m: not(inspect.isroutine(m)))
        # filter down to just properties
        props = [m for m in members if not(m[0][:2] == '__')]
        # format into django choice tuple
        choices = tuple([(str(p[1].value), p[0]) for p in props])
        return choices

class LoadFixture(object):

    def __init__(self, app_label, fixtures):
        self.app_label = app_label
        self.fixtures = fixtures

    def __call__(self, apps, schema_editor):
        if isinstance(self.fixtures, list):
            for fixture in self.fixtures:
                call_command('loaddata', fixture, app_label=self.app_label)
        else:
            call_command('loaddata', self.fixtures, app_label=self.app_label)

class UnloadFixture(object):

    def __init__(self, app_label):
        self.app_label = app_label

    def __call__(self, app, schema_editor):
        "Brutally deleting all entries for this model..."

        for model in app.get_models(self.app_label):
            model.objects.all().delete()

class ParamParser(object):

    def __init__(self, params, json_data=True):
        if json_data or isinstance(params, str):
            self.p = json.loads(params)
        else:
            self.p = params

    def get_val(self, k, default=''):
        return self.p[k].strip() if k in self.p else default

    def get_int(self, k, default=0):
        if k not in self.p:
            return default
        try:
            return int(self.p[k])
        except ValueError:
            return default

    def get_float(self, k, default=0.0):
        if k not in self.p:
            return default
        try:
            return float(self.p[k])
        except ValueError:
            return default

    def get_date(self, k, default=None):
        if k not in self.p:
            return default
        try:
            return datetime.strptime(self.p[k], '%Y-%m-%d').date()
        except ValueError:
            return default

    def get_datetime(self, k, default=None):
        if k not in self.p:
            return default
        try:
            return datetime.strptime(self.p[k], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return default

