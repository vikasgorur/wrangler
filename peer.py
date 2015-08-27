from twython import Twython, TwythonStreamer

class ConsolePeer:
    def send(self, text):
        "Send text to the peer"
        print(text)

    def input(self):
        "Get input from the peer"
        print('> ', end='')
        return input()

    def post(self, text):
        "Post a tweet"
        print("POST: {0}".format(text))

    def close(self):
        pass

class TwitterPeer(TwythonStreamer):
    def __init__(self, conf):
        super().__init__(conf.CONSUMER_KEY, conf.CONSUMER_SECRET,
            conf.OAUTH_TOKEN, conf.OAUTH_TOKEN_SECRET)
        self._client = Twython(conf.CONSUMER_KEY, conf.CONSUMER_SECRET,
            conf.OAUTH_TOKEN, conf.OAUTH_TOKEN_SECRET)
        self._handler_name = conf.HANDLER_NAME
        self._callback = None

    def on_success(self, data):
        if 'direct_message' in data:
            dm = data['direct_message']
            if dm['sender_screen_name'] == self._handler_name:
                self._callback.input(dm['text'])

    def on_error(self, status_code, data):
        print(status_code)
        self.disconnect()

    def send(self, text):
        "Send text via DM"
        self._client.send_direct_message(screen_name=self._handler_name, text=text)

    def listen(self, callback):
        """Listen to input via DM and invoke callback.input() when something is
           available"""

        if not self._callback:
            self._callback = callback
            self.user()

    def post(self, text):
        "Post a tweet"
        self._client.update_status(status=text)
        print("posting tweet: {0}".format(text))

    def close(self):
        self.disconnect()
