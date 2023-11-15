from django.http.request import HttpRequest
from django.http.response import HttpResponse


def sayHello(request):
    return HttpResponse("Hello World")
