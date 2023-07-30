from django.shortcuts import render, redirect
from django.db.models import Q
from django.http import HttpResponse
from .models import Room, Topic, Message
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .forms import RoomForm

def loginPage(request: any) -> HttpResponse:
    context = {'page' : 'login'}
    
    if request.user.is_authenticated:
        return redirect('home')

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

    return render(request, 'base/login_register.html', context)

def registerPage(request: any) -> HttpResponse:
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form' : form})

def logoutUser(request: any) -> any:
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
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()

    if request.method == 'POST':
        message = Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room' : room, 
        'room_messages' : room_messages,
        'participants' : participants
    }  

    return render(request, 'base/room.html', context)

@login_required(login_url='login')
def createRoom(request: any) -> HttpResponse:
    form = RoomForm()

    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form' : form} 

    return render(request, 'base/room_form.html', context) 

@login_required(login_url='login')
def updateRoom(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!!')

    form = RoomForm(instance=room)

    context = {'form' : form}

    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')

    return render(request, 'base/room_form.html', context)

@login_required(login_url='login') 
def deleteRoom(request: any, pk: str) -> HttpResponse:
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('You are not allowed here !!!')  

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    
    return render(request, 'base/delete.html', {'obj': room})

@login_required(login_url='login') 
def deleteMessage(request: any, pk: str) -> HttpResponse:
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here !!!')  

    if request.method == 'POST':
        message.delete()
        return redirect('room', pk=message.room.id)
    
    return render(request, 'base/delete.html', {'obj': room})
    