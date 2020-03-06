from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.conf import settings
from rest_framework.reverse import reverse as api_reverse
from django.db import models
import json


def string_to_list(string):
    stripped = []
    if type(string) != type([]):
        if string.find(',') != -1:
            for i in string.split(','):
                stripped.append(i.strip())
        else:
            stripped.append(string.strip())
        return stripped
    else:
        return string

class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, unique= True)

    def __str__(self):
        return str(self.name)

class Info(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    _tags = models.TextField(default='[]', blank=True)
    value = models.FloatField(default= 0)
    date = models.DateField()
    time = models.TimeField()

    @property
    def tags(self):
        return json.loads(self._tags)

    @tags.setter
    def tags(self, value):
        self._tags = json.dumps(string_to_list(value))

    def __str__(self):
        return str(f'{self.id},{self.user},{self.category},{self.tags},{self.value}, {self.date},{self.time}')
