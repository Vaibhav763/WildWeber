from django.contrib.messages.storage.base import Message
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserRating, Game, GameRating,Post,PostRating,Comment,PostReport,UserReport,GameReport,Follower,Following,CreatorNotification,UserNotification
from django.contrib import messages
import datetime
import random
# Create your views here.

def index(request):
    return render(request,'accounts/index.html')

def loginbase(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == "POST":
        mail = request.POST.get("inputEmail", '')
        passw = request.POST.get("inputPassword", '')
        try:
            us = User.objects.get(username = mail)
            val = authenticate(request, username = us, password = passw)
            if val is not None:
                login(request, us)
            else: 
                messages.info(request, 'Invalid Credentials')
                redirect('accounts:index')
        except:
            messages.error(request, 'It seems like you haven\'t joined our community yet. Register if you have not already.')
    return redirect('accounts:team')

def registerbase(request):
    if request.user.is_authenticated:
        return redirect('accounts:index')
    if request.method == "POST":
        fname = request.POST.get('firstName','')
        lname = request.POST.get('lastName','')
        print(fname, '+', lname)
        usnm = request.POST.get('username','')
        mail = request.POST.get('email','')
        passw = request.POST.get('address','')
        dobs = request.POST.get('dob', '')
        dob = datetime.datetime.strptime(dobs, "%Y-%m-%d").date()

        print(dobs)
        print(type(dobs))
        # try:
        us = User(username=usnm)
        us.email = mail
        us.first_name = fname
        us.last_name = lname
        us.set_password(passw)
        us.save()
        print('user created')
        prof = UserProfile(auth_user = us)
        prof.dob = dob
        prof.joined = datetime.datetime.now()
        prof.secretkey = random.randint(111111, 999999)
        prof.save()
        
        print('profile created')
        # except:
        #     messages.info(request, 'You are already in the community. Login to your account')
        #     print('some error')
        #     return redirect('accounts:index')
    return redirect('accounts:index')

def about(request):
    return render(request,'accounts/about.html')

def privacy(request):
    return render(request,'accounts/privacy.html')

def team(request):
    return render(request,'accounts/team.html')

def othersprofile(request):
    return render(request,'accounts/othersprofile.html')

def signup(request):
    return render(request,'accounts/signup.html')

def explore(request):
    return render(request,'accounts/explore.html')
