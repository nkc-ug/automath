from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(repuest):
    return render(repuest , "index.html")

def calculate(repuest,expr):
    response = "You typed " + expr + "."
    return HttpResponse(response)
