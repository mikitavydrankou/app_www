from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return HttpResponse("<h1>Привет, мир! Это моя страничка на Django!</h1>")