from django.utils.decorators import decorator_from_middleware
from django.middleware.gzip import GZipMiddleware

GZip = decorator_from_middleware(GZipMiddleware)
del GZipMiddleware