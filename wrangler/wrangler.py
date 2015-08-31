import logging
import pause
import sys

import datetime

from config import Config

from wrangler.conversation import Conversation
from wrangler.ebooks import EbooksText
from wrangler.peer import TwitterPeer, ConsolePeer

def validate_run_times(conf):
    if len(conf.RUN_AT) == 0:
        return False
        
    return all([0 <= h <= 23 and 0 <= m <= 60 for (h, m) in conf.RUN_AT])

def next_run_time(conf):
    now = datetime.datetime.now()
    (now_h, now_m) = now.hour, now.minute
    times = sorted(conf.RUN_AT)
    future_times = [(h, m) for (h, m) in times if h > now_h or h == now_h and m > now_m]
    if len(future_times) == 0:
        # nothing in the future today, so pick the first time tomorrow
        (h, m) = times[0]
        return datetime.datetime.combine(
            datetime.date.today() + datetime.timedelta(days=1),
            datetime.time(h, m))
    else:
        (h, m) = future_times[0]
        return datetime.datetime.combine(
            datetime.date.today(), datetime.time(h, m))

def main():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M')
    logger = logging.getLogger('main')
    logger.info('starting up')

    ebooks = EbooksText(Config)

    if not validate_run_times(Config):
        logger.error('invalid run times specified')
        sys.exit(1)

    while True:
        ebooks.update()
        peer = TwitterPeer(Config)
        conv = Conversation(ebooks, peer)

        next_run = next_run_time(Config)
        logger.info('sleeping until {0}'.format(next_run))
        pause.until(next_run)
        conv.talk()

if __name__ == '__main__':
    main()
