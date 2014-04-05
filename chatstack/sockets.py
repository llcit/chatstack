# chatstack/sockets.py
import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace
from django.contrib.auth.models import User
import pdb
from livethread.models import ThreadSpace,ThreadMessage


@namespace('/livethread')
class ThreadNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []

    def initialize(self):
        self.logger = logging.getLogger("socketio.livethread")
        self.log("Socketio session started")
        
    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
        print self.socket.sessid
    
    def on_join(self, room):
        self.room = room
        self.join(room)
        try: 
            self.socket.session['threadspace'] = ThreadSpace.objects.get(pk=room)
        except:
            self.broadcast_event('error', '%s is not valid activity and has disconnected' % room)
        self.log("Joining room.")
        return True
        
    def on_nickname(self, nickname):
        self.log('Connected nickname is: {0}'.format(nickname))
        self.nicknames.append(nickname)
        self.socket.session['nickname'] = nickname
        # pdb.set_trace()
        try:
            self.socket.session['DjangoUser']= User.objects.get(username=nickname)
        except:
            self.broadcast_event('error', '%s is not valid user and has disconnected' % nickname)
            self.disconnect(silent=True)
            return False
        # self.broadcast_event('announcement', '%s has connected' % nickname)
        # self.broadcast_event('nicknames', self.nicknames)
        return nickname

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        nickname = self.socket.session['nickname']
        self.nicknames.remove(nickname)
        self.broadcast_event('announcement', '%s has disconnected' % nickname)
        self.broadcast_event('nicknames', self.nicknames)
        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        # save to threadmessage model: threadspace, user, content
        self.log('User message: {0}'.format(msg))
        try:
            ThreadMessage(thread= self.session['threadspace'], user= self.session['DjangoUser'], text=msg).save()
            print "message successfully saved to database"
        except:
            pass
        self.emit_to_room(self.room, 'msg_to_room', self.socket.session['nickname'], msg)
        return True

