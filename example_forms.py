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
    <a href="/validate/">Form validation demo</a>
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

class DemoForm(djng.forms.Form):
    name = djng.forms.CharField(max_length = 100)
    email = djng.forms.EmailField()
    optional_text = djng.forms.CharField(required = False)

def validate(request):
    if request.method == 'POST':
        form = DemoForm(request.POST)
        if form.is_valid():
            return djng.Response('Form was valid: %s' % djng.escape(
                repr(form.cleaned_data)
            ))
    else:
        form = DemoForm()
    return djng.Response("""
    <form action="/validate/" method="post">
    %s
    <p><input type="submit">
    </form>
    """ % form.as_p())

app = djng.Router(
    (r'^$', index),
    (r'^search/$', search),
    (r'^submit/$', submit),
    (r'^validate/$', validate),
)

if __name__ == '__main__':
    djng.serve(app, '0.0.0.0', 8888)
