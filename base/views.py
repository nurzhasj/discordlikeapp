from django.shortcuts import render
from django.http import HttpResponse
from .models import Room

# Create your views here.
def home(request: any) -> HttpResponse:
    context = {'rooms' : Room.objects.all()}
    return render(request, 'base/home.html', context)

def room(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    
    context = {'room' : room}  

    return render(request, 'base/room.html', context)