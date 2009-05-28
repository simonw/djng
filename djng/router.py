from django.conf.urls.defaults import patterns
from django.core import urlresolvers

class Router(object):
    """
    Convenient wrapper around Django's urlresolvers, allowing them to be used 
    from normal application code.

    from django.http import HttpResponse
    from django_openid.request_factory import RequestFactory
    from django.conf.urls.defaults import url
    router = Router(
        url('^foo/$', lambda r: HttpResponse('foo'), name='foo'),
        url('^bar/$', lambda r: HttpResponse('bar'), name='bar')
    )
    rf = RequestFactory()
    print router(rf.get('/bar/'))
    """
    def __init__(self, *urlpairs):
        self.urlpatterns = patterns('', *urlpairs)
        # for 1.0 compatibility we pass in None for urlconf_name and then
        # modify the _urlconf_module to make self hack as if its the module.
        self.resolver = urlresolvers.RegexURLResolver(r'^/', None)
        self.resolver._urlconf_module = self
    
    def handle(self, request):
        path = request.path_info
        callback, callback_args, callback_kwargs = self.resolver.resolve(path)
        return callback(request, *callback_args, **callback_kwargs)
    
    def __call__(self, request):
        return self.handle(request)