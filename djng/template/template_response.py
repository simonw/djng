from djng.response import Response
from django.template import loader, RequestContext

class TemplateResponse(Response):
    def __init__(self, request, template, context = None):
        self.context = context or {}
        self.template = template
        self.request = request
        super(TemplateResponse, self).__init__()
    
    def get_container(self):
        return [
            loader.get_template(self.template).render(
                RequestContext(self.request, self.context)
            )
        ]
    
    def set_container(self, *args):
        pass # ignore
    
    _container = property(get_container, set_container)
