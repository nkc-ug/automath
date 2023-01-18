from django.shortcuts import render
from django.http import HttpResponse
from . import main

# Create your views here.
def index(repuest):
    return render(repuest , "index.html")

def calculate(repuest,expr):
    return HttpResponse(main.calculation(expr))
