from django.core.management.base import BaseCommand

import json
from metrics.models import Info, Category
import urllib.request
from django.contrib.auth import authenticate
import re
import datetime
import random
import json
from faker import Faker
fake = Faker()

class Command(BaseCommand):
    help = 'Populate DB with random values'

    def add_arguments(self, parser):
        parser.add_argument('generates', type=int)
        parser.add_argument('user', type=str)
        parser.add_argument('pass', type=str)

    def handle(self, *args, **kwargs):
        json_data = []
        tags = [fake.word() for _ in range(1,50)]
        user = authenticate(username=kwargs['user'], password=kwargs['pass'])
        categories = Category.objects.all()

        if user:
            if len(categories) == 0:
                for _ in range(0,random.randint(0,10)):
                    Category.objects.create(user=user,name=fake.word())
                categories = Category.objects.all()

            for _ in range(1, kwargs['generates']):
                category = random.choice(categories)
                random_tags = list(set(random.choices(tags, k= random.randint(1,10))))
                if len(random_tags) == 1:
                    random_tags = random_tags[0]
                else:
                    random_tags = random_tags
                date = str(fake.date_between_dates(date_start=datetime.date(2000, 1, 1), date_end=datetime.date(2020, 12, 12)))
                value = round(random.uniform(-100,100),4)
                time = fake.time(pattern='%I:%M %p', end_datetime=None)

                Info.objects.create(user=user,
                                    category= category,
                                    _tags= json.dumps(random_tags),
                                    date= date,
                                    value= value,
                                    time= time)

                json_data.append({'user': user.username,
                                  'category': category.name,
                                  'tags': random_tags,
                                  'value': value,
                                  'date': date,
                                  'time': time})

        else:
            print('Username or password incorrect')

        if len(json_data):
            file = open('saved_data.json','w')
            file.write(str(json.dumps(json_data, indent= 2)))
            file.close()