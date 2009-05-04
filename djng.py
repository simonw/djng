"""
Just some sketched out ideas at the moment, this code has never been executed.
"""

from django import http
from django.core import signals
from django.utils.encoding import force_unicode
from django.utils.importlib import import_module

from django.conf.urls.defaults import patterns
from django.core import urlresolvers
from django.core.handlers.wsgi import STATUS_CODE_TEXT, WSGIRequest

import sys

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
        self.resolver = urlresolvers.RegexURLResolver(r'^/', self)
    
    def handle(self, request):
        path = request.path_info
        callback, callback_args, callback_kwargs = self.resolver.resolve(path)
        return callback(request, *callback_args, **callback_kwargs)
    
    def __call__(self, request):
        return self.handle(request)

class Handler(object):
    # Changes that are always applied to a response (in this order).
    response_fixes = [
        http.fix_location_header,
        http.conditional_content_removal,
        http.fix_IE_for_attach,
        http.fix_IE_for_vary,
    ]
    request_middleware = []
    response_middleware = []
    exception_middleware = []
    
    debug = False
    propagate_exceptions = False
    
    def __init__(self, router):
        self.router = router
    
    def __call__(self, environ, start_response):
        try:
            request = WSGIRequest(environ)
        except UnicodeDecodeError:
            response = http.HttpResponseBadRequest()
        else:
            response = self.get_response(request)

            # Apply response middleware
            for middleware_method in self.response_middleware:
                response = middleware_method(request, response)
            response = self.apply_response_fixes(request, response)

        try:
            status_text = STATUS_CODE_TEXT[response.status_code]
        except KeyError:
            status_text = 'UNKNOWN STATUS CODE'
        status = '%s %s' % (response.status_code, status_text)
        response_headers = [(str(k), str(v)) for k, v in response.items()]
        for c in response.cookies.values():
            response_headers.append(('Set-Cookie', str(c.output(header=''))))
        start_response(status, response_headers)
        return response
    
    def get_response(self, request):
        "Returns an HttpResponse object for the given HttpRequest"
        from django.core import exceptions, urlresolvers

        # Apply request middleware
        for middleware_method in self.request_middleware:
            response = middleware_method(request)
            if response:
                return response
        
        # Resolve and execute the view, catching any errors
        try:
            response = self.router(request)
        except Exception, e:
            # If the view raised an exception, run it through exception
            # middleware, and if the exception middleware returns a
            # response, use that. Otherwise, reraise the exception.
            for middleware_method in self.exception_middleware:
                response = middleware_method(request, e)
                if response:
                    return response
            raise
        except http.Http404, e:
            return self.handle_404(request, e)
        except exceptions.PermissionDenied:
            return self.handle_permission_denied(request)
        except SystemExit:
            # Allow sys.exit() to actually exit. See tickets #1023 and #4701
            raise
        except: # Handle everything else, including SuspiciousOperation, etc.
            # Get exc_info now, in case another exception is thrown later
            exc_info = sys.exc_info()
            receivers = signals.got_request_exception.send(
                sender=self.__class__, request=request
            )
            return self.handle_uncaught_exception(request, exc_info)

    def handle_404(self, request, e):
        if self.debug:
            from django.views import debug
            return debug.technical_404_response(request, e)
        else:
            return http.HttpResponseNotFound('<h1>404</h1>')
    
    def handle_permission_denied(self, request):
        return http.HttpResponseForbidden('<h1>Permission denied</h1>')

    def handle_uncaught_exception(self, request, exc_info):
        """
        Processing for any otherwise uncaught exceptions (those that will
        generate HTTP 500 responses). Can be overridden by subclasses who want
        customised 500 handling.

        Be *very* careful when overriding this because the error could be
        caused by anything, so assuming something like the database is always
        available would be an error.
        """
        from django.core.mail import mail_admins

        if self.propagate_exceptions:
            raise

        if self.debug:
            from django.views import debug
            return debug.technical_500_response(request, *exc_info)

        # When DEBUG is False, send an error message to the admins.
        subject = 'Error: %s' % request.path
        try:
            request_repr = repr(request)
        except:
            request_repr = "Request repr() unavailable"
        message = "%s\n\n%s" % (self._get_traceback(exc_info), request_repr)
        mail_admins(subject, message, fail_silently=True)
        # Return an HttpResponse that displays a friendly error message.
        return self.handle_500(request, exc_info)

    def _get_traceback(self, exc_info=None):
        "Helper function to return the traceback as a string"
        import traceback
        return '\n'.join(
            traceback.format_exception(*(exc_info or sys.exc_info()))
        )

    def apply_response_fixes(self, request, response):
        """
        Applies each of the functions in self.response_fixes to the request 
        and response, modifying the response in the process. Returns the new
        response.
        """
        for func in self.response_fixes:
            response = func(request, response)
        return response

def serve(handler, host='localhost', port=6789):
    from django.core.servers.basehttp import run
    run(host, int(port), handler)
