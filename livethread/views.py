from socketio import socketio_manage

from django.shortcuts import render
from django.views.generic import DetailView

from .models import ThreadSpace
from chatstack.sockets import ThreadNamespace

class ThreadSpaceView(DetailView):
    model =  ThreadSpace
    template_name = 'threadspace.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ThreadSpaceView, self).get_context_data(**kwargs)
    #     context['thread_id'] = self.get_object().id
    #     return context

