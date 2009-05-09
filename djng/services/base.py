from manager import ServiceManager

class ServiceConfigurationError(Exception):
    pass


def proxy(methodname, servicemanager):
    def method(self, *args, **kwargs):
        return getattr(servicemanager.current(), methodname)(*args, **kwargs)
    return method

class ServiceMeta(type):
    def __new__(cls, name, bases, attrs):
        # First add service manager instance to attrs
        attrs['service'] = ServiceManager()
        # All attrs methods are converted in to proxies
        for key, value in attrs.items():
            if callable(value):
                # TODO: inspect funcargs, copy them and the docstring so that 
                # introspection tools will tell us correct arguments
                attrs[key] = proxy(key, attrs['service'])
        return super(ServiceMeta, cls).__new__(cls, name, bases, attrs)

class Service(object):
    __metaclass__ = ServiceMeta
