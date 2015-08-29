import logging
import subprocess

import config

class EbooksText:
    def __init__(self, conf):
        self.generate_cmd = conf.EBOOKS_GENERATE.split()
        self.update_cmds = [cmd.split() for cmd in conf.EBOOKS_UPDATE]
        self.logger = logging.getLogger(self.__class__.__name__)

    def update(self):
        for cmd in self.update_cmds:
            try:
                output = subprocess.check_output(cmd, universal_newlines=True, stderr=subprocess.STDOUT).strip()
                for line in output.split("\n"):
                    self.logger.info('update: {0}'.format(line))
            except Exception as e:
                self.logger.error('update failed: {0}'.format(e))
                return

    def generate(self):
        try:
            return subprocess.check_output(self.generate_cmd, universal_newlines=True).strip()
        except Exception as e:
            return None

if __name__ == '__main__':
    e = EbooksText(config.Config)
    print(e.generate())
