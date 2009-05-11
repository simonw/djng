from djng import services
from djng.services.cache import CacheConfigure

# Default service configuration
services.configure('cache', CacheConfigure(
    in_memory = True,
))
# Or maybe this:
#     services.cache.configure(CacheConfigure(in_memory = True))
# Or even:
#     services.cache.configure(in_memory = True)
# Or...
#     services.default('cache', InMemoryCache())
# Or...
#     services.configure('cache', InMemoryCache())

def app(request):
    from djng.services.cache import cache
    counter = cache.get('counter')
    if not counter:
        counter = 1
    else:
        counter += 1
    cache.set('counter', counter)
    print counter

app(None)
app(None)

# Middleware that reconfigures service for the duration of the request
app = services.wrap(app, 'cache', InMemoryCache())

# Or...
app = services.wrap(app, 
    cache = InMemoryCache(),
)


app(None)
app(None)
app(None)
    