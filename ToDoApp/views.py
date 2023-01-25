from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import TodoForm
from .models import Todo


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


def create_todo(request):
    if request.method == 'GET':
        return render(request, 'ToDoApp/create_todo.html', context={'form': TodoForm()})
    elif request.method == 'POST':
        form = TodoForm(request.POST)
        if form.is_valid():
            new_todo = form.save(commit=False)
            new_todo.user = request.user
            new_todo.save()
            return redirect('current_todos')
        else:
            return render(request, 'ToDoApp/create_todo.html',
                          context={'form': TodoForm(), 'error': 'Bad data inputed'})


def current_todos(request):
    todos = Todo.objects.filter(user=request.user, date_completion__isnull=True)
    return render(request, 'ToDoApp/current_todos.html', context={'todos': todos})


def view_todo(request, pk):
    todo = get_object_or_404(Todo, id=pk, user=request.user)
    form = TodoForm(instance=todo)
    if request.method == 'GET':
        return render(request, 'ToDoApp/current_todo.html', context={'todo': todo, 'form': form})
    elif request.method == 'POST':
        return update_todo(request, todo)


def update_todo(request, todo):
    todo = TodoForm(request.POST, instance=todo)
    if todo.is_valid():
        todo.save()
        return render(request, 'ToDoApp/current_todo.html', context={'todo': todo, 'form': todo})
    else:
        return render(request, 'ToDoApp/current_todo.html',
                      context={'todo': todo, 'form': todo, 'error': 'bad info'})


def complete_todo(request, pk):
    if request.method == 'POST':
        todo = get_object_or_404(Todo, id=pk, user=request.user)
        todo.date_completion = timezone.now()
        todo.save()
        return redirect('current_todos')
