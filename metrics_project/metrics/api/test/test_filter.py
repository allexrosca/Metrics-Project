from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from metrics.models import *
import datetime
import json
from metrics.api.views import InfoFilter

strptime = datetime.datetime.strptime
strftime = datetime.datetime.strftime

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

    def test_filter_item_by_one_tag(self):
        data = {'tags':'here'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 1)
        self.assertIn(data['tags'],result[0].tags)

    def test_filter_item_by_multiple_tags(self):
        data = {'tags':['2','to put']}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 2)
        for tag in data['tags']:
            self.assertIn(tag,result[0].tags)

    def test_filter_item_by_category(self):
        data = {'category':'second'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 1)
        self.assertEqual(str(result[0].category), data['category'])

    def test_filter_item_by_date_after(self):
        data = {'date_after':'2020-2-2'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 1)
        self.assertGreaterEqual(result[0].date, strptime(data['date_after'],'%Y-%m-%d').date())

    def test_filter_item_by_date_before(self):
        data = {'date_before':'2020-2-2'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 2)
        for i in result:
            self.assertLessEqual(i.date, strptime(data['date_before'],'%Y-%m-%d').date())

    def test_filter_item_by_time_after(self):
        data = {'time_after':'1:00 PM'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 2)
        for i in result:
            self.assertGreaterEqual(strftime(strptime(str(i.time),'%H:%M:%S'),'%I:%M %p'),
                                    strftime(strptime(data['time_after'], '%I:%M %p'), '%I:%M %p'))

    def test_filter_item_by_time_before(self):
        data = {'time_after': '12:00 PM'}

        qs = Info.objects.all()
        filter = InfoFilter(data=data, queryset=qs)
        result = filter.qs
        self.assertEqual(result.count(), 2)
        self.assertLessEqual(strftime(strptime(str(result[0].time), '%H:%M:%S'), '%I:%M %p'),
                                strftime(strptime(data['time_after'], '%I:%M %p'), '%I:%M %p'))