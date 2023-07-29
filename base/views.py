from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from .forms import RoomForm

# Create your views here.
def home(request: any) -> HttpResponse:
    query = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__contains = query) |
        Q(name__contains = query) |
        Q(description__contains = query)
    )
    topics = Topic.objects.all()
    room_count = rooms.count()

    context = {'rooms' : rooms, 'topics' : topics, 'room_count' : room_count}

    return render(request, 'base/home.html', context)

def room(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)
    
    context = {'room' : room}  

    return render(request, 'base/room.html', context)

def createRoom(request: any) -> HttpResponse:
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form} 

    return render(request, 'base/room_form.html', context) 

def updateRoom(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    form = RoomForm(instance=room)

    context = {'form' : form}

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', context)

def deleteRoom(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})
    