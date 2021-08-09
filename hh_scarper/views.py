from django.http.response import HttpResponse


def index(request):
    return HttpResponse('<h1>Whoaa!<h1>')
