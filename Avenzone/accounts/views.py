from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'accounts/index.html')

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
