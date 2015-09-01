import logging
import queue

from collections import namedtuple

import tweepy

# A typed message sent by the stream listener.
# The type can either be 'error' or 'input'
Message = namedtuple('Message', ['type', 'value'])

class PeerError(Exception):
    pass

class ConsolePeer:
    def send(self, text):
        "Send text to the peer"
        print(text)

    def input(self):
        "Get input from the peer"
        print('> ', end='')
        try:
            return input()
        except KeyboardInterrupt as e:
            raise PeerError(e)

    def post(self, text):
        "Post a tweet"
        print("POST: {0}".format(text))

class DmListener(tweepy.StreamListener):
    def __init__(self, handler_name, q):
        super().__init__()
        self._handler_name = handler_name
        self._q = q

    def on_direct_message(self, status):
        if status.direct_message['sender_screen_name'] == self._handler_name:
            self._q.put(Message(type='input', value=status.direct_message['text']))

    def on_error(self, status_code):
        if status_code >= 500:
            self._q.put(Message(type='error', value=None))

class TwitterPeer:
    def __init__(self, conf):
        self._handler_name = conf.HANDLER_NAME
        self._logger = logging.getLogger('{0}.{1}'.format(__name__, self.__class__.__name__))

        auth = tweepy.OAuthHandler(conf.CONSUMER_KEY, conf.CONSUMER_SECRET)
        auth.set_access_token(conf.OAUTH_TOKEN, conf.OAUTH_TOKEN_SECRET)

        self._api = tweepy.API(auth)
        self._q = queue.Queue()
        self._stream = tweepy.Stream(auth=auth,
            listener=DmListener(self._handler_name, self._q))
        self._stream.userstream(async=True)

    def send(self, text):
        "Send text via DM"
        self._logger.info('sending DM to {0}: {1}'.format(self._handler_name, text))
        self._api.send_direct_message(screen_name=self._handler_name, text=text)

    def input(self):
        (t, val) = self._q.get()
        if t == 'input':
            return val
        elif t == 'error':
            raise PeerError(val)

    def listen(self, callback):
        """Listen to input via DM and invoke callback.input() when something is
           available"""

        if not self._callback:
            self._callback = callback
            self._logger.info('started listening to user stream')
            self.user()

    def post(self, text):
        "Post a tweet"
        self._api.update_status(text)
        self._logger.info('posting tweet: {0}'.format(text))
