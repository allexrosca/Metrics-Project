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

    # --- NOT AUTHENTICATED ---

    def test_put_item_not_auth(self):
        data = {'category': 'random',
                'value': 2,
                'date': datetime.date(2020, 1, 1),
                'tag':'no',
                'time': '11:12PM'
                }
        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # --- AUTHENTICATED ---

    def test_put_item_auth(self):
        data = {'category': 'second',
                'value': 1,
                'date': datetime.date(1999, 1, 1),
                'tags':'added, tags, here',
                'time': '5:30 AM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})

        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_item_auth_removing_tags(self):
        data = {'category': 'second',
                'value': 1,
                'date': datetime.date(1999, 1, 1),
                'tags':'',
                'time': '5:30 AM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_put_item_auth_wrong_tags(self):
        data = {'category': 'second',
                'value': 21,
                'date': datetime.date(2000, 1, 1),
                'tags':['random1','random2',],
                'time': '5:30AM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_item_auth_wrong_date_format(self):
        data = {'category': 'second',
                'value': 21,
                'date': '23-23-2000',
                'tags': 'randomTag',
                'time': '5:30AM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_item_auth_wrong_time_format(self):
        data = {'category': 'second',
                'value': 21,
                'date': datetime.date(2000, 1, 1),
                'tags': 'randomTag',
                'time': '23:32:00'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_item_auth_not_existing_category(self):
        data = {'category': 'nope',
                'value': 21,
                'date': datetime.date(2000, 1, 1),
                'tags': 'randomTag',
                'time': '3:00AM'
                }

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk':1})
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_put_item_different_user(self):
        data = {'category': 'random',
                'value': 10.213123,
                'date': datetime.date(2050, 10, 10),
                'tags':'other user',
                'time': '5:30AM'
                }


        user = User(username='testuser2', email='test@t2.com')
        user.set_password('testpassword')
        user.save()

        original_item = Info.objects.first()

        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk': 1})
        response = self.client.put(url, data, format='json')

        modified_item = Info.objects.first()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotEqual(original_item.user, modified_item.user)
        self.assertEqual(modified_item.user.username, user.username)
