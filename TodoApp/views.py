from django.shortcuts import render

# Create your views here.
def login(request):
    data={}
    return render(request,'login.html',data)

def homepage(request):
    data={}
    return render(request,'homepage.html',data)

def signUp(request):
    data={}
    data["error"]="Please enter valid username and password"
    return render(request,'signup.html',data)

def resetPassword(request):
    data={}
    return render(request,'resetPassword.html',data)

def profilePage(request):
    data={}
    return render(request,'profilePage.html',data)

def logOut(request):
    data={}
    return render(request,'login.html',data)

