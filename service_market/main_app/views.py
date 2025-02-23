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
from .models import AppUser, UserLog, Announcement

def landing_page(request):
    if request.user.is_authenticated:
        announcements = Announcement.objects.order_by("-pub_date")
        print('announcments', announcements)
        context = {
            "announcements" : announcements,
            "user" : request.user,
        }
        usr = AppUser.objects.get(user=request.user)
        log = UserLog(user=usr, action_time=datetime.now(), action='announcement')
        log.save()
        return render(request, "main_app/landing_page.html", context)
    else:
        return HttpResponseRedirect('/main_app/login')


def register(request):
    if request.method == "GET":
        return render(request, "main_app/register.html", {})
    else:
        try:
            name = request.POST['name']
            email = request.POST["email"]
            password = request.POST["password"]
            repeat_password = request.POST["repeat_password"]
        except:
            return render(request, "main_app/register.html", {"error_message": "Missed Field"})        

        if password != repeat_password:
            return render(request, "main_app/register.html", {"error_message": "Password not match."})        

        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.save()
        
        poll_user = AppUser(user=user, email=email)
        poll_user.save()

    return  HttpResponseRedirect('/main_app/login/')

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
        usr = AppUser.objects.get(user=user)
        log = UserLog(user=usr, action_time=datetime.now(), action='login')
        log.save()
        return HttpResponseRedirect('/main_app/')

    else:
        return render(request, "main_app/login.html", {"error_message": "Email or password is incorrect."}) 



def logout(request):
    _logout(request)
    return HttpResponseRedirect("/main_app/login")



def announcement_detail(request, id):
    announcement = get_object_or_404(Announcement, id=id)
    return render(request, 'main_app/detail.html', {'announcement': announcement})


def add_announcement(request):
    if request.user.is_authenticated:
        if request.method == "GET":
            return render(request, 'main_app/add_announcement.html', {})
        else:
            user = request.user
            auser = AppUser.objects.get(user=user)
            description = request.POST["description"]
            title = request.POST['title']
            contact_info = request.POST['contact_info']
            image = request.POST['image']

            a = Announcement(author=auser,
                description=description,
                title=title,
                image=image,
                contact_info=contact_info,
                pub_date=datetime.now()
            )
            a.save()
            return HttpResponseRedirect("/main_app/announcement/" + str(a.id))

    else:
        return HttpResponseRedirect("/main_app/login")