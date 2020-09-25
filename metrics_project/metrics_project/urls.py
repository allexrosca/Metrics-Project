from django.contrib import admin
from django.conf.urls import url, include

urlpatterns = [
    url('admin/', admin.site.urls),
    url(r'^api/', include('metrics.api.urls', namespace='api')),
    url(r'^metrics/', include('metrics.urls', namespace='metrics')),
]
