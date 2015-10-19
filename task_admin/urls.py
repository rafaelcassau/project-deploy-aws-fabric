from django.conf.urls import patterns, include, url
from django.contrib import admin
from tasks.api import TaskResource


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/tasks/', include(TaskResource.urls()))
)
