from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError


def home(request):
    return render(request, 'ToDoApp/home.html')


def logout_user(request):
    logout(request)
    return render(request, 'ToDoApp/home.html')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/signupuser.html', context={'form': UserCreationForm()})
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
            except IntegrityError:
                return render(request, 'ToDoApp/signupuser.html', context={'form': UserCreationForm(),
                                                                           'error': 'This username is already exist'})
            login(request, user)
            return redirect('current_todos')
        else:
            return render(request, 'ToDoApp/signupuser.html', context={'form': UserCreationForm(),
                                                                       'error': 'Passwords did not match'})


def login_user(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/login_user.html', context={'form': AuthenticationForm()})
    elif request.method == 'POST':

        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('current_todos')
        else:
            return render(request, 'ToDoApp/login_user.html', context={'form': AuthenticationForm(),
                                                                       'error': 'Username and password did not math'})


def current_todos(request):
    return render(request, 'ToDoApp/current_todos.html')
