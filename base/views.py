from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import RoomForm

def loginPage(request: any) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exists")
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password doesn't exists")

    return render(request, 'base/login_register.html', {})

def logoutUser(request: any) -> HttpResponse:
    logout(request)
    return redirect('home')

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
    