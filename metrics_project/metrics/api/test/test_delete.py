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

    def test_delete_item_not_auth(self):
        data = {}
        url = api_reverse('api:info_rud_item', kwargs={'pk': 1})
        response = self.client.delete(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    # --- AUTHENTICATED ---

    def test_delete_item_auth(self):
        data = {}

        user = User.objects.first()
        payload = payload_handler(user)
        token = encode_handler(payload)
        self.client.credentials(HTTP_AUTHORIZATION='JWT ' + token)

        url = api_reverse('api:info_rud_item', kwargs={'pk': 1})
        response = self.client.delete(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, None)

        info = Info.objects.all()
        self.assertEqual(info.count(),2)
