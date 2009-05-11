import djng

def index(request):
    return djng.Response('Hello, world')

if __name__ == '__main__':
    djng.serve(index, '0.0.0.0', 8888)
