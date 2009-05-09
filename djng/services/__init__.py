"""
Services
--------

Services are classes that can have their underlying implementation swapped out
at runtime.

"""

class Service(object):
    implementation = None

class TemplateService(Service):
    def render(self, template, context):
        return template % context
