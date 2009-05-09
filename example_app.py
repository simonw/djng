from djng.services.cache import CacheConfigure

def view(request):
    from djng.services.cache import cache
    counter = cache.get('counter')
    if not counter:
        counter = 1
    else:
        counter += 1
    cache.set('counter', counter)
    print counter

app = CacheConfigure(
    in_memory = True,
    next = view
)

app(None)
app(None)
app(None)
app(None)
app(None)
    