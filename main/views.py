from django.shortcuts import render
from django.http import HttpResponse


def function1(response , id):
    return HttpResponse("%d"  %id)

# Create your views here.
