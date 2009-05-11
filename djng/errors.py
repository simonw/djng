from django.http import Http404
from response import Response

class ErrorWrapper(object):
    def __init__(self, app, custom_404 = None, custom_500 = None):
        self.app = app
        self.error_404 = custom_404 or self.default_error_404
        self.error_500 = custom_500 or self.default_error_404
    
    def __call__(self, request):
        try:
            response = self.app(request)
        except Http404, e:
            return self.error_404(request)
        except Exception, e:
            return self.error_500(request, e)
        return response
    
    def default_error_404(self, request):
        return Response('A 404 error occurred')
    
    def default_error_500(self, request, e):
        return Response('A 500 error occurred: %r' % e)
