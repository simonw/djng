# First we have to monkey-patch django.core.handlers.base because 
# get_script_name in that module has a dependency on settings which bubbles 
# up to affect WSGIRequest and WSGIHandler
from django.utils.encoding import force_unicode
def get_script_name(environ):
    script_url = environ.get('SCRIPT_URL', u'')
    if not script_url:
        script_url = environ.get('REDIRECT_URL', u'')
    if script_url:
        return force_unicode(script_url[:-len(environ.get('PATH_INFO', ''))])
    return force_unicode(environ.get('SCRIPT_NAME', u''))
from django.core.handlers import base
base.get_script_name = get_script_name

# Now on with the real code...
from django import http
from django.core.handlers.wsgi import STATUS_CODE_TEXT, WSGIRequest
import sys

class WSGIWrapper(object):
    # Changes that are always applied to a response (in this order).
    response_fixes = [
        http.fix_location_header,
        http.conditional_content_removal,
        http.fix_IE_for_attach,
        http.fix_IE_for_vary,
    ]
    def __init__(self, view):
        self.view = view
    
    def __call__(self, environ, start_response):
        request = WSGIRequest(environ)
        response = self.view(request)
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
    
    def apply_response_fixes(self, request, response):
        """
        Applies each of the functions in self.response_fixes to the request 
        and response, modifying the response in the process. Returns the new
        response.
        """
        for func in self.response_fixes:
            response = func(request, response)
        return response

from django.core.servers.basehttp import \
    WSGIRequestHandler as WSGIRequestHandlerOld, \
    BaseHTTPRequestHandler, WSGIServer

class WSGIRequestHandler(WSGIRequestHandlerOld):
    def __init__(self, *args, **kwargs):
        self.path = ''
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)
    
    def log_message(self, format, *args):
        sys.stderr.write(
            "[%s] %s\n" % (self.log_date_time_string(), format % args)
        )

def serve(view, host='localhost', port=6789):
    httpd = WSGIServer((host, port), WSGIRequestHandler)
    httpd.set_app(WSGIWrapper(view))
    httpd.serve_forever()
