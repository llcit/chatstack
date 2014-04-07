# chatstack/sockets.py
# import gevent
# import gevent.monkey
# gevent.monkey.patch_all()

import logging

from socketio.namespace import BaseNamespace
from socketio.mixins import RoomsMixin, BroadcastMixin
from socketio.sdjango import namespace
from django.contrib.auth.models import User
# import pdb
from livethread.models import ThreadSpace,ThreadMessage

# from django.contrib.auth.models import User
# from livethread.models import ThreadSpace, ThreadMessage


import psycogreen.gevent
psycogreen.gevent.patch_psycopg()

import psycopg2


@namespace('/livethread')
class ThreadNamespace(BaseNamespace, RoomsMixin, BroadcastMixin):
    nicknames = []
    django_user = ''
    db_connection = ''
    db_cursor = ''

    def initialize(self):
        self.logger = logging.getLogger("socketio.livethread")
        self.log("Socketio session started")
        self.db_connection = psycopg2.connect(
            "dbname=csdb user=djangodbuser password=1 host=localhost")
        self.db_cursor = self.db_connection.cursor()

    def log(self, message):
        self.logger.info("[{0}] {1}".format(self.socket.sessid, message))
        print self.socket.sessid

    def on_join(self, room):
        self.room = room
        self.join(room)
        # try: 
        #     self.socket.session['threadspace'] = ThreadSpace.objects.get(pk=room)
        # except:
        #     self.broadcast_event('error', '%s is not valid activity and has disconnected' % room)
        # self.log("Joining room.")
        return True

    def on_nickname(self, nickname):
        self.log('Connected nickname is: {0}'.format(nickname))
        self.nicknames.append(nickname)
        self.socket.session['nickname'] = nickname

## Added by Richard
        self.db_cursor.execute(
            "select id from auth_user where username = %s;", (nickname,))
        self.django_user = self.db_cursor.fetchone()[0]


## Added by Hao
        # pdb.set_trace()
        # try:
        #     self.socket.session['DjangoUser']= User.objects.get(username=nickname)
        # except:
        #     self.broadcast_event('error', '%s is not valid user and has disconnected' % nickname)
        #     self.disconnect(silent=True)
        #     return False



        # self.broadcast_event('announcement', '%s has connected' % nickname)
        # self.broadcast_event('nicknames', self.nicknames)
        return nickname

    def recv_disconnect(self):
        # Remove nickname from the list.
        self.log('Disconnected')
        nickname = self.socket.session['nickname']
        self.nicknames.remove(nickname)

        # self.broadcast_event('announcement', '%s has disconnected' % nickname)
        # self.broadcast_event('nicknames', self.nicknames)
        self.db_cursor.close()
        self.db_connection.close()

        self.disconnect(silent=True)
        return True

    def on_user_message(self, msg):
        # save to threadmessage model: threadspace, user, content
## Added by Richard
        self.db_cursor.execute(
            "INSERT INTO livethread_threadmessage (thread_id, user_id, text) VALUES (%s, %s, %s)",
            (self.room, self.django_user, msg))
        self.db_connection.commit()


## Added by Hao
        # self.log('User message: {0}'.format(msg))
        # try:
        #     ThreadMessage(thread= self.session['threadspace'], user= self.session['DjangoUser'], text=msg).save()
        #     print "message successfully saved to database"
        # except:
        #     pass


        self.emit_to_room(self.room, 'msg_to_room', self.socket.session['nickname'], msg)
        return True

        self.log('User message SAVED.: {0}'.format(msg))
        self.emit_to_room(self.room, 'msg_to_room',
                          self.socket.session['nickname'], msg)
        return True
