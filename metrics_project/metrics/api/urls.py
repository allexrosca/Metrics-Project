from django.conf.urls import url

from .views import *

app_name = 'api'

urlpatterns = [
    url(r'^info/$', InfoListView.as_view(), name='info_list_items'),
    url(r'^info/(?P<pk>\d+)/$', InfoRudView.as_view(), name='info_rud_item'),
    url(r'^info/post/$', InfoPostView.as_view(), name='info_post_item'),

    url(r'^category/$', CategoryListView.as_view(), name='category_list_items'),
    url(r'^category/(?P<pk>\d+)/$', CategoryRudView.as_view(), name='category_rud_item'),
    url(r'^category/post/$', CategoryPostView.as_view(), name='category_post_item'),
]