from django.contrib import admin

from livethread.models import ThreadSpace, ThreadMessage

admin.site.register(ThreadSpace)
admin.site.register(ThreadMessage)