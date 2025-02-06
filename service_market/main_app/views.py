#
import json

#
from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as _login, logout as _logout
from datetime import datetime

from .models import User, UserLog, Announcment



def landing_page(request):
    if request.user.is_authenticated:
        my_announcments = Announcment.objects.filter(author__user=request.user).order_by("-pub_date")
        other_announcments = Announcments.objects.exclude(author__user=request.user).order_by("-pub_date")
        context = {
            "my_announcments": my_announcments,
            "other_announcments": other_announcments,
            "user": request.user,
        }
        usr = User.objects.get(user=request.user)
        log = UserLog(user=usr, action_time=datetime.now(), action='question')
        log.save()
        return render(request, "main_app/landing_page.html", context)
    else:
        return HttpResponseRedirect('/main_app/login')


def register(request):
    if request.method == "GET":
        return render(request, "main_app/register.html", {})
    else:
        try:
            first_name = request.POST["firstname"]
            last_name = request.POST["lastname"]
            email = request.POST["email"]
            country = request.POST["country"]
            password = request.POST["password"]
            repeat_password = request.POST["repeat_password"]
        except:
            return render(request, "main_app/register.html", {"error_message": "Missed Field"})        

        if password != repeat_password:
            return render(request, "main_app/register.html", {"error_message": "Password not match."})


def login(request):
    if request.method == "GET":
        return render(request, 'main_app/login.html', {})
    else:
        try:
            email = request.POST["email"]
            password = request.POST["password"]
        except:
            return render(request, "main_app/login.html", {"error_message": "Missed Field"}) 
        
    user = authenticate(username=email, password=password)
    print("USER", email, password)
    if user:
        _login(request, user)
        usr = User.objects.get(user=user)
        log = UserLog(user=usr, action_time=datetime.now(), action='login')
        log.save()
        return HttpResponseRedirect('/main_app/')

    else:
        return render(request, "main_app/login.html", {"error_message": "Email or password is incorrect."}) 



def logout(request):
    _logout(request)
    return HttpResponseRedirect("/main_site/login")