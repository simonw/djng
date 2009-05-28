djng
====
(pronounced "djing", with a mostly-silent "d")

Blog entry: http://simonwillison.net/2009/May/19/djng/
Mailing list: http://groups.google.com/group/djng

djng is a micro-framework that depends on a macro-framework (Django).

My definition of a micro-framework: something that lets you create an entire
Python web application in a single module:

    import djng
    
    def index(request):
        return djng.Response('Hello, world')
    
    if __name__ == '__main__':
        djng.serve(index, '0.0.0.0', 8888)

Or if you want hello and goodbye URLs, and a custom 404 page:

    import djng

    app = djng.ErrorWrapper(
        djng.Router(
            (r'^hello$', lambda request: djng.Response('Hello, world')),
            (r'^goodbye$', lambda request: djng.Response('Goodbye, world')),
        ),
        custom_404 = lambda request: djng.Response('404 error', status=404),
        custom_500 = lambda request: djng.Response('500 error', status=500)
    )
    
    if __name__ == '__main__':
        djng.serve(app, '0.0.0.0', 8888)

Under the hood, djng will re-use large amounts of functionality from Django,
while re-imagining various aspects of the framework. A djng request object is
a Django HttpRequest object; a djng response object is a Django HttpResponse.
Django's template language and ORM will be available. Ideally, Django code
will run almost entirely unmodified under djng, and vice versa.

Services, not Settings
======================

I dislike Django's settings.py file - I often find I want to reconfigure
settings at run-time, and I'm not comfortable with having arbitrary settings
for so many different aspects of the framework.

djng experiments with /services/ in place of settings. Services are bits of
shared functionality that djng makes available to applications - for example,
caching, templating, ORM-ing and mail-sending.

Most of the stuff that Django sets up in settings.py will in djng be set up by
configuring services. These services will be designed to be reconfigured at
run-time, using a mechanism similar to Django middleware.

Some things that live in settings.py that really don't belong there -
middleware for example. These will generally be constructed by composing
together a djng application in code.

I'm still figuring out how the syntax for services should work.
