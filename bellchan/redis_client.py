import redis
from bellchan.settings import Settings


class RedisClient:

    def __init__(self, db=0):
        self._parse_and_set_url(Settings.REDIS_URL)
        self._db = db

        self._r = self._create_redis()

    def _parse_and_set_url(self, redis_url):
        self._redis_url = redis_url

        _, _, password_and_host, port = self._redis_url.split(':')
        password, host = password_and_host.split('@')

        self._host = host
        self._port = port
        self._password = password

    def _create_redis(self):
        return redis.StrictRedis(host=self._host,
                                 port=self._port,
                                 db=self._db,
                                 password=self._password)

    def set(self, key, value):
        return self._r.set(key, value)

    def get(self, key):
        return self._r.get(key)

    def incr(self, key):
        return self._r.incr(key)
