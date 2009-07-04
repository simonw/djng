from template_response import TemplateResponse
from django.conf import settings

def configure(template_dirs):
    if isinstance(template_dirs, basestring):
        template_dirs = [template_dirs]
    settings.TEMPLATE_DIRS = template_dirs
