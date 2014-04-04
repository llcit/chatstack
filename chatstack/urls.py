from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import socketio.sdjango
socketio.sdjango.autodiscover()

from livethread.views import ThreadSpaceView

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'livethread.views.home', name='home'),
	url(r'^socket\.io', include(socketio.sdjango.urls)),

	url(r'^thread/(?P<pk>\d+)$', ThreadSpaceView.as_view(), name='thread'),

    url(r'^admin/', include(admin.site.urls)),
)
