from django.shortcuts import render
from django.http import HttpResponse

rooms = [
    {'id': 1, 'name': 'Let us learn python together'},
    {'id': 2, 'name': 'Golang developers'},
    {'id': 3, 'name': 'JavaScript mastery course'},
    {'id': 3, 'name': 'C fundamentals'},
]

# Create your views here.
def home(request: any) -> HttpResponse:
    context = {'rooms' : rooms}
    return render(request, 'base/home.html', context)

def room(request: any, pk: str) -> HttpResponse:
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
    context = {'room' : room} 

    return render(request, 'base/room.html', context)