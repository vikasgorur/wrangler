

class ConsolePeer:
    def send(self, text):
        "Send text to the peer"
        print(text)

    def input(self):
        print('> ', end='')
        return input()

    def post(self, text):
        "Post a tweet"
        print("POST: {0}".format(text))

class TwitterPeer:
    pass
