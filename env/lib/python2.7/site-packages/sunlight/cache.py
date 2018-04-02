'''
.. module:: cache

The cache is disabled by default. Use it like so: ::

    import logging
    from sunlight import response_cache
    response_cache.enable('mongo')
    response_cache.logger.setLevel(logging.DEBUG)

Note: the implementation below doesn't bother with cache expiration.
Typical use case is caching API calls during an expensive build process.
'''
import pickle
import logging
import functools


backends = {}


class _BackendMeta(type):
    def __new__(meta, name, bases, attrs):
        cls = type.__new__(meta, name, bases, attrs)
        backends[name] = cls
        shortname = name.lower().replace('backend', '')
        backends[shortname] = cls
        for nickname in attrs.get('nicknames', []):
            backends[nickname] = cls
        return cls


class BaseBackend(object):
    __metaclass__ = _BackendMeta

    def check(self, key):
        '''Try to return something from the cache.
        '''
        raise NotImplementedError()

    def set(self, key, val):
        '''Set something in the cache.
        '''
        raise NotImplementedError()

    def purge(self, *keys):
        '''Try to purge one or more things from the cache.
        If keys is empty, purges everything.
        '''
        raise NotImplementedError()


class MemoryBackend(BaseBackend):
    '''In-memory cache for API responses.
    '''
    nicknames = ['mem', 'locmem', 'localmem']

    def __init__(self):
        self._cache = {}

    def check(self, key):
        return self._cache.get(key)

    def set(self, key, val):
        self._cache[key] = val

    def purge(self, *keys):
        if not keys:
            self._cache = {}
        map(self._cache.pop, keys)


class MongoBackend(BaseBackend):
    '''Mongo cache of API respones.
    '''
    def __init__(self):
        self.mongo = get_mongo()

    def check(self, key):
        doc = self.mongo.responses.find_one(key)
        if doc:
            return doc['v']

    def set(self, key, val):
        doc = dict(_id=key, v=val)
        self.mongo.responses.save(doc)

    def purge(self, *keys):
        if not keys:
            spec = {}
        else:
            spec = {'_id': {'$in': keys}}
        self.mongo.reponses.remove(spec)


class BaseCache(object):

    def __init__(self):
        self.backend = None
        self.logger = logging.getLogger('cache')
        ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        ch.setFormatter(formatter)
        self.logger.addHandler(ch)

    def set_backend(self, backend_name):
        try:
            self.backend = backends[backend_name]()
            self.logger.info('Changed cache backend to %r.' % self.backend)
        except KeyError:
            raise ValueError('No backend named %r is defined.' % backend_name)

    enable = set_backend

    def disable(self):
        '''Disable the cache. Will wipe out an in-memory cache.
        '''
        self.backend = None
        self.logger.info('Response caching disabled.')

    def purge(self):
        '''Wipe out the cache.
        '''
        self.logger.info('Purging cache...')
        self.backend.purge()
        self.logger.info('...done.')

    def get_key(self, *args, **kwargs):
        '''Create a cache key based on the input to the wrapped callable.
        '''
        raise NotImplementedError()

    def __call__(self, method):
        '''Returns a class decorator.
        '''
        cache = self

        @functools.wraps(method)
        def memoizer(self, *args, **kwargs):
            # If no backend is set, do nothing.
            if cache.backend is None:
                return method(self, *args, **kwargs)
            key = cache.get_key(self, *args, **kwargs)
            val = cache.backend.check(key)
            if val is None:
                cache.logger.debug(' MISS %r' % [self, args, kwargs])
                val = method(self, *args, **kwargs)
                cache.backend.set(key, val)
            else:
                cache.logger.debug(' HIT %r' % [self, args, kwargs])
            return val
        return memoizer


class ResponseCache(BaseCache):
    '''Simple cache implementation with pickled strings as cache keys.
    '''

    def get_key(self, method_self, *args, **kwargs):
        '''Create a cache key by: pickle.dumps((module, name, args, kwargs))
        '''
        name = self.__class__.__name__
        module = self.__class__.__module__
        key = pickle.dumps((module, name, args, kwargs))
        return key


response_cache = ResponseCache()


def get_mongo():
    try:
        import pymongo
    except ImportError:
        msg = 'The mongo cache backend requires pymongo.'
        raise ImportError(msg)
    from sunlight import config
    host = getattr(config, 'MONGO_HOST', None)
    dbname = getattr(config, 'MONGO_DATABASE_NAME', 'pythonsunlight_cache')
    conn = pymongo.MongoClient(host=host)
    mongo = getattr(conn, dbname)
    return mongo
