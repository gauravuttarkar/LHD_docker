
from django.http import HttpResponse
from django.shortcuts import render, redirect
#from . import templates
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib import auth
#from events.models import bankDetails

