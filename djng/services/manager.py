import threading

class ServiceNotConfigured(Exception):
    # TODO: This needs to indicate WHICH service is not configured
    pass

class ServiceManager(threading.local):
    """
    A ServiceManager keeps track of the available implementations for a 
    given service, and which implementation is currently the default. It 
    provides methods for registering new implementations and pushing and 
    popping a stack representing the default implementation.
    """
    def __init__(self, default_implementation=None):
        self.clear_stack()
        if default_implementation is not None:
            self.push(default_implementation)
        
    def clear_stack(self):
        self._stack = []
    
    def push(self, impl):
        self._stack.insert(0, impl)
    
    def pop(self):
        return self._stack.pop(0)
    
    def current(self):
        if not self._stack:
            raise ServiceNotConfigured
        return self._stack[0]
