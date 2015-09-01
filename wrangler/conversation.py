import logging
import sys

from config import Config

from wrangler.ebooks import EbooksText
from wrangler.peer import ConsolePeer, TwitterPeer

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

    def _interpret(self, choice):
        # Twitter won't let you send the same message twice within a
        # short duration. So we tolerate extra junk after the command.
        if choice.startswith('0') or choice.lower().startswith('n'):
            return True
        elif choice.isdigit() and 1 <= int(choice) <= self.batch_size:
            self.peer.post(self._tweets[int(choice) - 1])
            self.peer.send('Tweet {0} posted.'.format(int(choice)))
            return False
        elif choice.lower().startswith('q'):
            self.peer.send('bye')
            return False
        else:
            self.peer.send('Unknown command, aborting conversation.')
            return False

    def talk(self):
        "Talk to the handler once by sending tweets and waiting for input"

        while True:
            self._tweets = self.generate_tweets(self.batch_size)
            self.peer.send('\n'.join(
                ['{0}. {1}'.format(i+1, self._tweets[i]) for i in range(self.batch_size)]))

            if not self._interpret(self.peer.input()):
                break

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    ebooks = EbooksText(Config)
    peer = TwitterPeer(Config) if len(sys.argv) == 2 and sys.argv[1] == 'twitter' else ConsolePeer()
    conv = Conversation(ebooks, peer)
    conv.talk()
