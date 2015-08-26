import twython

from config import Config
from ebooks import EbooksText
from peer import ConsolePeer, TwitterPeer


class Conversation:
    """A conversation starts with the bot messaging the handler with a list
    of potential tweets. This continues back and forth until the handler
    chooses a tweet or aborts the conversation."""

    def __init__(self, ebooks, peer):
        self.ebooks = ebooks
        self.peer = peer
        self.batch_size = 5

    def generate_tweets(self, n):
        "Generate n tweets using the ebooks text generator"
        return [self.ebooks.generate() for i in range(n)]

    def run(self):
        "Run this conversation from start to finish"

        while True:
            tweets = self.generate_tweets(self.batch_size)
            self.peer.send('\n'.join(
                ['{0}. {1}'.format(i+1, tweets[i]) for i in range(self.batch_size)]))

            choice = self.peer.input()

            if choice == '0' or choice == 'n':
                continue
            elif choice.isdigit() and 0 < int(choice) < self.batch_size:
                self.peer.post(tweets[int(choice) - 1])
                self.peer.send('Tweet {0} posted.', int(choice))
            else:
                self.peer.send('Unknown command, aborting conversation.')
                break

if __name__ == '__main__':
    #client = twython.Twython(conf.CONSUMER_KEY, conf.CONSUMER_SECRET,
    #    conf.OAUTH_TOKEN, conf.OAUTH_TOKEN_SECRET)

    ebooks = EbooksText(Config)
    conv = Conversation(ebooks, ConsolePeer())
    conv.run()
