# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static


urlpatterns = patterns('',
    #url(r'^dashboard/', include('api.dashboard.urls', namespace='dashboard')),
    url(r'^user/', include('api.user.urls', namespace='user')),
    url(r'^member/', include('api.member.urls', namespace='member')),
)