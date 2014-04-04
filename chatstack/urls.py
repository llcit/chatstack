from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import socketio.sdjango
socketio.sdjango.autodiscover()

from livethread.views import ThreadSpaceView, ThreadListView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'livethread.views.home', name='home'),
	url(r'^socket\.io', include(socketio.sdjango.urls)),

	url(r'^threads$', ThreadListView.as_view(), name='threads'),
	url(r'^thread/(?P<pk>\d+)$', ThreadSpaceView.as_view(), name='thread'),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),

    url(r'^admin/', include(admin.site.urls)),
)
