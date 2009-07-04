import djng, os, datetime

djng.template.configure(
    os.path.join(os.path.dirname(__file__), 'example_templates')
)

def index(request):
    return djng.TemplateResponse(request, 'example.html', {
        'time': str(datetime.datetime.now()),
    })

if __name__ == '__main__':
    djng.serve(index, '0.0.0.0', 8888)
