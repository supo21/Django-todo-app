from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import TODO


# Create your views here.
def home(request):
    return render(request, "signup.html")

def signup(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = User.objects.create(
            username = name,
            email = email,
        )

        user.set_password(password)
        user.save()
        return redirect('/login')
    
    return render(request, 'signup.html')


def user_login(request):
    if request.method == "POST":
        name = request.POST.get('name')
        password = request.POST.get("password")
        
        user = authenticate(request, username = name, password=password)

        if user is None:
            return redirect('/login')
        else:
            login(request, user)
            return redirect('/todo')
        
    return render(request, 'login.html')

def todo(request):
    if request.method == "POST":
        title = request.POST.get("title")
        task = TODO(title = title, user=request.user)
        task.save()
        user = request.user
        alltask = TODO.objects.filter(user=user).order_by('-date')
        context = {"alltask":alltask}
        return redirect('/todo', context)
    
    user = request.user
    alltask = TODO.objects.filter(user=user).order_by('-date')
    context = {"alltask":alltask}
    return render(request, 'todo.html', context)


def signout(request):
    logout(request)
    return redirect('/login')


def update_todo(request, sno):
    if request.method == "POST":
        title = request.POST.get('title')
        task = TODO.objects.get(sno = sno)
        task.title = title
        task.save()
        return redirect('/todo')
    
    task = TODO.objects.get(sno = sno)
    context = {"task" : task}
    return render(request, 'edit_todo.html', context)

def delete_todo(request, sno):
    task = TODO.objects.get(sno = sno)
    task.delete()
    return redirect('/todo')