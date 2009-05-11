from django.http import HttpResponse as HttpResponseOld
from Cookie import SimpleCookie

class HttpResponse(HttpResponseOld):
    default_charset = 'utf8'
    def __init__(self, content='', status=None, content_type=None):
        if not content_type:
            content_type = 'text/html; charset=%s' % self.default_charset
        if not isinstance(content, basestring) and\
                hasattr(content, '__iter__'):
            self._container = content
            self._is_string = False
        else:
            self._container = [content]
            self._is_string = True
        self.cookies = SimpleCookie()
        if status:
            self.status_code = status
        self._headers = {'content-type': ('Content-Type', content_type)}
