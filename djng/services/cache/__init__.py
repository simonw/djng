from djng.services.base import Service, ServiceConfigurationError

class CacheConfigure(object):
    def __init__(self, next, impl=None, in_memory=False):
        self.next = next
        if impl and in_memory:
            raise ServiceConfigurationError, 'Only one of impl or in_memory'
        if not (impl or in_memory):
            raise ServiceConfigurationError, 'One of impl or in_memory reqd.'
        if in_memory:
            impl = DictCache()
        self.impl = impl
    
    def __call__(self, *args, **kwargs):
        cache.service.push(self.impl)
        try:
            return self.next(*args, **kwargs)
        finally:
            obj = cache.service.pop()
            assert obj == self.impl, 'Popped the wrong cache implementation!'

class CacheService(Service):
    def get(self, key):
        pass
    
    def set(self, key, value):
        pass

class DictCache(object):
    def __init__(self):
        self._d = {}
    
    def get(self, key):
        return self._d.get(key)
    
    def set(self, key, value):
        self._d[key] = value

class UpperDictCache(DictCache):
    def get(self, key):
        return self._d.get(key, '').upper()

cache = CacheService()