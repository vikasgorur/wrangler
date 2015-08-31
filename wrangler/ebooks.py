import datetime
import logging
import subprocess
import os
import time

import config

class EbooksText:
    def __init__(self, conf):
        self.generate_cmd = conf.EBOOKS_GENERATE.split()
        self.update_cmds = [cmd.split() for cmd in conf.EBOOKS_UPDATE]
        self.logger = logging.getLogger(self.__class__.__name__)

    def _update_required(self):
        """Return true if it's been 12 hours since last update or we don't know
        when the last update was"""

        if not os.path.isfile('.last_updated'): return True

        with open('.last_updated') as f:
            try:
                last_updated = datetime.datetime.fromtimestamp(float(f.readline()))
            except:
                self.logger.info('update: don\'t know when last corpus update was, updating')
                return True

            if datetime.datetime.now() - last_updated > datetime.timedelta(hours=12):
                self.logger.info('update: last corpus update was at {0}, updating'.format(last_updated))
                return True
            else:
                self.logger.info('update: last corpus update was at {0}, not updating'.format(last_updated))
                return False

    def _write_timestamp(self):
        with open('.last_updated', mode='w') as f:
            f.write(str(time.time()))

    def update(self):
        if not self._update_required(): return

        for cmd in self.update_cmds:
            try:
                output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT).strip()
                for line in output.split("\n"):
                    self.logger.info('update: {0}'.format(line))
            except Exception as e:
                self.logger.error('update failed: {0}'.format(e))
                return

        self._write_timestamp()

    def generate(self):
        try:
            return subprocess.check_output(self.generate_cmd, universal_newlines=True).strip()
        except Exception as e:
            return None

if __name__ == '__main__':
    e = EbooksText(config.Config)
    print(e.generate())
