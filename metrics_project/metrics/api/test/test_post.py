from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework.reverse import reverse as api_reverse
from metrics.models import *
from rest_framework import status
from rest_framework_jwt.settings import api_settings
import datetime
import json

strptime = datetime.datetime.strptime
strftime = datetime.datetime.strftime

payload_handler = api_settings.JWT_PAYLOAD_HANDLER
encode_handler = api_settings.JWT_ENCODE_HANDLER

class InfoTestCase(APITestCase):
    def setUp(self):
        user = User(username='testuser', email='test@t.com')
        user.set_password('testpassword')
        user.save()
        Category.objects.create(user= user,
                                name= 'random')
        Category.objects.create(user= user,
                                name= 'second')
        Info.objects.create(user= user,
                            category= Category.objects.get(name='random'),
                            _tags= json.dumps('what tags, to put, here, 2'),
                            value= 5,
                            date= datetime.date(2000, 1, 1),
                            time= strptime('10:00 AM', '%I:%M %p'))
        Info.objects.create(user= user,
                            category= Category.objects.get(name='second'),
                            value= 532,
                            date= datetime.date(2222, 1, 1),
                            time= strptime('8:32 PM', '%I:%M %p'))
        Info.objects.create(user= user,
                            category= Category.objects.get(name='random'),
                            _tags= json.dumps('one, 2, to put'),
                            value= -5.5123,
                            date= datetime.date(1900, 12, 12),
                            time= strptime('3:00 PM', '%I:%M %p'))

    # Basics
    def test_single_user(self):
        user_count = User.objects.count()
        self.assertEqual(user_count,1)

    def test_info(self):
        info = Info.objects.count()
        self.assertEqual(info,3)

    # --- NOT AUTHENTICATED ---

    def test_post_item_not_auth(self):
        data = {'category': 'random',
                'value': 300,
                'date': datetime.date(2000, 1, 1),
                'tag':'random tags, with, Space',
                'time': '9:12 AM'
                }
        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info, 3)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



    # --- AUTHENTICATED ---

    def test_post_item_auth_without_tags(self):
        data = {'category': 'random',
                'value': 144,
                'date': datetime.date(2020, 11, 21),
                'time': '11:12 PM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info,4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_item_auth_with_tags(self):
        data = {'category': 'random',
                'value': 144,
                'date': datetime.date(2020, 11, 21),
                'tags': 'the, tags are,   right here                    ',
                'time': '5:00PM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info,4)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_item_auth_with_wrong_tags(self):
        data = {'category': 'random',
                'value': 144,
                'date': datetime.date(2020, 11, 21),
                'tags': 'the, tags are,',
                'time': '5:00PM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info,3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_item_auth_with_not_existing_category(self):
        data = {'category': 'notExistingCat',
                'value': 144,
                'date': datetime.date(2020, 11, 21),
                'tags': 'the, tags are',
                'time': '5:00PM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info,3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_item_auth_with_wrong_date(self):
        data = {'category': 'random',
                'value': 144,
                'date': '23-23-200',
                'tags': 'the, tags are',
                'time': '5:00PM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info, 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_item_auth_with_wrong_time(self):
        data = {'category': 'random',
                'value': 144,
                'date': datetime.date(2020, 11, 21),
                'tags': 'the, tags are',
                'time': '23:00'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info, 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_item_auth_with_no_required_values(self):
        data = {'tags': 'the, tags are'}

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_post_item')
        response = self.client.post(url, data, format='json')
        info = Info.objects.count()

        self.assertEqual(info, 3)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)