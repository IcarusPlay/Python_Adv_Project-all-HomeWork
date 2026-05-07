from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

# Create your views here.

def greetings(request:HttpRequest ) -> HttpResponse:
    return HttpResponse("Hello, world. You're at the polls page.")