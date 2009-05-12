import djng

def index(request):
    return djng.Response("""
    <h1>Forms demo</h1>
    <form action="/search/" method="get">
        <p>
            <input type="search" name="q">
            <input type="submit" value="Search">
        </p>
    </form>
    <form action="/submit/" method="post">
        <p><textarea name="text" rows="5" cols="30"></textarea></p>
        <p><input type="submit" value="Capitalise text"></p>
    </form>
    """)

def search(request):
    return djng.Response(
        "This page would search for %s" % djng.escape(
            request.GET.get('q', 'no-search-term')
        )
    )

def submit(request):
    text = request.POST.get('text', 'no-text')
    return djng.Response(djng.escape(text.upper()))

app = djng.Router(
    (r'^$', index),
    (r'^search/$', search),
    (r'^submit/$', submit),
)

if __name__ == '__main__':
    djng.serve(app, '0.0.0.0', 8888)
