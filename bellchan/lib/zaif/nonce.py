from logging import getLogger
import os
from bellchan.path import Path

logger = getLogger(__name__)


class ZaifNonce:

    NONCE_FILE = '.nonce'

    def __init__(self):
        self.path = os.path.join(Path.ROOT_PATH, self.NONCE_FILE)

        if not os.path.exists(self.path):
            self._init_file()

    def _init_file(self):
        with open(self.path, 'w') as f:
            f.write('0')

    def get(self):
        with open(self.path, 'r+') as f:
            old_nonce_str = f.read().strip()
            logger.info(f'Get nonce {old_nonce_str}')

            nonce = int(old_nonce_str) + 1
            nonce_str = str(nonce)

            f.seek(0)
            f.write(nonce_str)
            logger.info(f'Update nonce to {nonce_str}')

        return nonce
