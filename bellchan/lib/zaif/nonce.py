from bellchan.redis_client import RedisClient


class ZaifNonce:

    KEY = 'zaif_nonce'

    def __init__(self):
        self.redis = RedisClient()

    def get(self):
        return self.redis.incr(self.KEY)
