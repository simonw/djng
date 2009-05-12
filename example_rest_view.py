import djng

class RestView(object):
    def __call__(self, request, *args, **kwargs):
        method = request.method.upper()
        if hasattr(self, method):
            return getattr(self, method)(request, *args, **kwargs)
        return self.method_not_supported(request)
    
    @staticmethod
    def method_not_supported(request):
        return djng.Response('Method not supported')
    

class MyView(RestView):
    @staticmethod
    def GET(request):
        return djng.Response('This is a GET')
    
    @staticmethod
    def POST(request):
        return djng.Response('This is a POST')

if __name__ == '__main__':
    djng.serve(MyView(), '0.0.0.0', 8888)
