from django.contrib.messages.storage.base import Message
from django.http import request
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import UserProfile, UserRating, Game, GameRating, Post, PostRating, Comment, PostReport, UserReport, GameReport, Follower, Following, CreatorNotification, UserNotification
from django.contrib import messages
import datetime
import random
# Create your views here.


def index(request):
    if request.user.is_authenticated:
        print(type(request.user))
        return redirect('accounts:home')

    return render(request, 'accounts/index.html')


def loginbase(request):
    if request.method == "POST":
        mail = request.POST.get("inputEmail", '')
        print(mail)
        passw = request.POST.get("inputPassword", '')
        try:
            us = User.objects.get(username=mail)
        except:
            us = None
            messages.error(
                request, 'It seems like you haven\'t joined our community yet. Register if you have not already.')
            print('some error')
        val = authenticate(request, username=us, password=passw)
        if val is not None:
            login(request, us)
            return redirect('accounts:home')
        else:
            print("invalid creds")
            messages.info(request, 'Invalid Credentials')
            redirect('accounts:index')

    return redirect('accounts:index')


def registerbase(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    if request.method == "POST":
        fname = request.POST.get('firstName', '')
        lname = request.POST.get('lastName', '')
        print(fname, '+', lname)
        usnm = request.POST.get('username', '')
        mail = request.POST.get('email', '')
        passw = request.POST.get('address', '')
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
        prof = UserProfile(auth_user=us)
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
    return render(request, 'accounts/about.html')


def privacy(request):
    return render(request, 'accounts/privacy.html')


def team(request):
    return render(request, 'accounts/team.html')


def othersprofile(request):
    return render(request, 'accounts/othersprofile.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    return render(request, 'accounts/signup.html')


def explore(request):
    games = Game.objects.all()
    params = {'games': games}
    return render(request, 'accounts/explore.html',  params)


def verification(request):
    return render(request, 'accounts/verification.html')


def feedback(request):
    return render(request, 'accounts/feedback.html')


def password(request):
    if request.user.is_authenticated:
        return render(request, 'accounts/password.html')
    return redirect('accounts:index')


def passwordbase(request):
    if request.user.is_authenticated:
        us = request.user
        if request.method == "POST":
            npassw = request.POST.get('address', '')
            print(npassw)
            us.set_password(npassw)
            us.save()
            messages.success(request, 'Password Updated Successfully!')
            print("corrected")
            return redirect('accounts:home')
        return redirect('accounts:password')
    return redirect('account:index')


def terms(request):
    return render(request, 'accounts/terms.html')


def home(request):
    return render(request, 'accounts/home.html')


def logoutbase(request):
    logout(request)
    return redirect("accounts:index")


def follow(request):
    return render(request, 'accounts/follow.html')

def notification(request):
    return render(request, 'accounts/notification.html')

def profile(request):
    return render(request, 'accounts/profile.html')
