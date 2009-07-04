# Some settings are just too much work to monkey-patch around
from django.conf import settings
settings.configure(USE_18N = False)
del settings

import middleware
from django.conf.urls.defaults import url
from router import Router
from errors import ErrorWrapper
from response import Response
from wsgi import serve
from django import forms
from django.utils.html import escape
from django.utils.safestring import mark_safe
import template
from template import TemplateResponse
