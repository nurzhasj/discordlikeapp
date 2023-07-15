from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request: any):
    return render(request, 'home.html')