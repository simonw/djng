import djng

def hello(request):
    return djng.Response('Hello, world ' * 100)

def goodbye(request):
    return djng.Response('Goodbye, world ' * 100)

app = djng.Router(
    (r'^hello$', hello),
    (r'^goodbye$', djng.middleware.GZip(goodbye)),
)

if __name__ == '__main__':
    djng.serve(app, '0.0.0.0', 8888)
