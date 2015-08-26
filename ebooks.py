import subprocess

import config

class EbooksText:
    def __init__(self, config):
        self.cmd = config.EBOOKS_COMMAND.split()

    def generate(self):
        try:
            return subprocess.check_output(self.cmd, universal_newlines=True).strip()
        except Exception as e:
            return None

if __name__ == '__main__':
    e = EbooksText(config.Config)
    print(e.generate())
