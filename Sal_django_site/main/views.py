from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .models import InfoPrompt
# Create your views here.

def homepage(request):
    return render(request=request,
                  template_name="main/home.html",
                  context={"InfoPrompt": InfoPrompt.objects.all})
def contact(request):
    return render(request=request,
                  template_name="main/contact.html")#,
                 # context={"InfoPrompt": InfoPrompt.objects.all})

def login_request(request):
    return render(request=request,
                  template_name="main/login.html")

def signup(request):
    return render(request=request,
                  template_name="main/signup.html")

def logout_request(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("main:homepage")