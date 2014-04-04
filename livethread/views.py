from socketio import socketio_manage

from django.shortcuts import render
from django.views.generic import DetailView, TemplateView

from braces.views import LoginRequiredMixin

from .models import ThreadSpace
from chatstack.sockets import ThreadNamespace

class ThreadListView(LoginRequiredMixin, TemplateView):
    template_name = 'threads.html'
        
class ThreadSpaceView(LoginRequiredMixin, DetailView):
    model =  ThreadSpace
    template_name = 'threadspace.html'

