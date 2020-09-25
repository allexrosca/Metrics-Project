from django.conf.urls import url

from .views import *

app_name = 'metrics'

urlpatterns = [
    url(r'^$', DashboardHome.as_view(), name='dashboardHome'),
]