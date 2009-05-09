class Configure(object):
    def __init__(self, next, **kwargs):
        """
        **kwargs should have keys that are names of services and value that 
        are implementations of those services.
        """
        for name, impl in kwargs.items():
            self.get_service(name).push(impl)
    
    def get_service(self, name):
        # TODO: implement this
        pass

        