from django.shortcuts import render
from .forms import PostForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from . import templates
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
#from events.models import bankDetails
from django.contrib.auth import logout as django_logout
	
# Create your views here.

def home(request):
    print("Home")
    return render(request, 'landing/index.html', {'user':request.user})




def login1(request):
    """
    Return login page
    """

    return render(request,'landing/login.html')

def logout(request):
    """
    Return logout page
    """
    django_logout(request)
    print("Logging out")
    return redirect('/')


def signup(request):
    """
    Return sign up page
    """
    return render(request,'landing/signup.html')


def signup_submit(request):
    """
    function which runs after clicking sign up submit
    """
    print("Creating a new user")
    username = request.POST.get('username')
    password = request.POST.get('password')
    email = request.POST.get('email')
    if username == '' or password == '' or email == "":
        return render(request,'landing/signup.html')

    user = User.objects.create_user(username=username, email=email,password=password)
    user.save()

    return redirect('/')



def logging_in(request):
    """
    Function which runs after log in button is pressed

    """
    username = request.POST['username']
    password = request.POST['password']
    if username == '' or password == '':
        return render(request,'landing/login.html')
    user = authenticate(request, username=username, password=password)
    print(user)
    if user is not None:
        login(request,user)
        return redirect('/',{'user':request.user})
        # Redirect to a success page.
        ...
    else:
        return redirect('/login')
        # Return an 'invalid login' error message.
        ...