from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt

from .models import Room, Topic, Message, User
from .forms import RoomForm, UserForm, MyUserCreationForm

import json
import requests
import asyncio
import threading
import socket
import os
import time

from pydantic import BaseModel, Field
from typing import List, Union

from dotenv import load_dotenv
from langchain_ollama import OllamaEmbeddings
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModel



def run_ollama_server():
    async def run_process(cmd):
        print('>>> starting', *cmd)
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        # Define an async pipe function
        async def pipe(lines):
            async for line in lines:
                print(line.decode().strip())

        # Run the pipes for stdout and stderr
        await asyncio.gather(pipe(process.stdout), pipe(process.stderr))

    async def start_ollama_serve():
        await run_process(['ollama', 'serve'])

    def run_async_in_thread(loop, coro):
        asyncio.set_event_loop(loop)
        loop.run_until_complete(coro)
        loop.close()

    # Helper function to check if a port is open
    def is_port_open(port):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            try:
                s.connect(('localhost', port))
                return True
            except ConnectionRefusedError:
                return False
    new_loop = asyncio.new_event_loop()
    # Start ollama serve in a separate thread so the function won't block execution
    thread = threading.Thread(target=run_async_in_thread, args=(new_loop, start_ollama_serve()))
    thread.start()
    print("Waiting for the Ollama server to start...")
    # Check if the server is running, retrying for up to 10 seconds
    for _ in range(10):  # Check for up to 10 seconds
        if is_port_open(11434):
            print("Ollama server is running.")
            return
    print("Ollama server did not start in time.") 

def generate_response(model: str, prompt: str, host: str = "localhost", port: int = 11434):
    """
    Sends a request to generate a response from a model using the provided prompt.
    """
    run_ollama_server()
    url = f"http://{host}:{port}/api/generate"
    headers = {"Content-Type": "application/json"}
    payload = {
    "model": model,
    "prompt": "you are a helpful ai assistant your responses should be long and if asked should provide the whole object list in zeroshot  list items should be seperated by commas  do not use phrases like Here is a list of ten notable Neoclassical paintings: this just list objects when asked like apple, banana, orange, etc     length of response 200 words  "+prompt,
    "stream": False,
    "options": {
            "num_predict": 150,
            "top_k": 50,
            "top_p": 0.95,
            "temperature": 0.7,
            "repeat_penalty": 1.2,
            "presence_penalty": 0.5,
            "frequency_penalty": 0.5,
            "stop": ["\n", "user:"],
            "num_ctx": 2048,
            "num_thread": 4
    }
}
    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()

        return response.json()

    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    ai_response = None
    if request.method == 'POST':
        # Check if the AI interaction form was submitted
        if 'ai_input' in request.POST:
            prompt = request.POST.get('ai_input')
            # Generate response using the AI model
            ai_response_data = generate_response(model="mistral", prompt=prompt)
            print(f"AI Response Data: {ai_response_data}")
            ai_response = ai_response_data.get("response", "Error generating response.")
        else:
            # Handle regular message creation
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'ai_response': ai_response
    }
    return render(request, 'base/room.html', context)
# traditional viewspage

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username OR password does not exit')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()  # Ensure username is lowercase
            user.save()
            
            # Log the user in immediately after registration
            login(request, user)
            
            # You could redirect to different pages based on the user’s role or profile.
            return redirect('home')  # Or any other page
        else:
            # Displaying specific error messages for validation issues
            for field in form.errors:
                messages.error(request, f"Error in {field}: {form.errors[field][0]}")
    
    return render(request, 'base/login_register.html', {'form': form})


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''

    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)
    )

    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:3]

    context = {'rooms': rooms, 'topics': topics,
               'room_count': room_count, 'room_messages': room_messages}
    return render(request, 'base/home.html', context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()
    participants = room.participants.all()
    ai_response = None
    if request.method == 'POST':
        # Check if the AI interaction form was submitted
        if 'ai_input' in request.POST:
            prompt = request.POST.get('ai_input')
            # Generate response using the AI model
            ai_response_data = generate_response(model="mistral", prompt=prompt)
            print(f"AI Response Data: {ai_response_data}")
            ai_response = ai_response_data.get("response", "Error generating response.")
        else:
            # Handle regular message creation
            message = Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
        'ai_response': ai_response
    }
    return render(request, 'base/room.html', context)




def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all()
    room_messages = user.message_set.all()
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms,
               'room_messages': room_messages, 'topics': topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)

        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
        )
        return redirect('home')

    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': room})


@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('Your are not allowed here!!')

    if request.method == 'POST':
        message.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj': message})


@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'base/update-user.html', {'form': form})


def topicsPage(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})


def activityPage(request):
    room_messages = Message.objects.all()
    return render(request, 'base/activity.html', {'room_messages': room_messages})






