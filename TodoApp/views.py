from django.shortcuts import render,redirect
from .models import *

# Create your views here.
def login(request):
    if request.session.has_key('username'):
        return redirect('homepage')
    else:
        data = {'error': None }
        if request.session.has_key('userdata'):
            return redirect('homepage')

        else:
            if request.method == 'POST':
                username = request.POST['username']
                password = request.POST['password']

                x = TaskMate_userDetails.objects.filter(username=username, password=password).values().exists()
                if x:
                    request.session['username']=username
                    return redirect('homepage')
                else:
                    data['error'] = "Invalid Credentials"
                    return render(request, 'login.html', data)

            return render(request, 'login.html')

def homepage(request):
    data={}
    if request.session.has_key('username'):
        username = request.session['username']
        if(request.method == "POST"):
            q_data = request.POST
            user=request.session['username']
            date=q_data.get('date')
            time=q_data.get('time')
            priority=q_data.get('priority')
            description=q_data.get('description')

            try:
                task=TaskMate_taskDetails(userName=user,deadlineDate=date,deadlineTime=time,priority=priority,description=description)
                task.save()
            except Exception as e:
                print(e)


        try:
            orderbyList = ['deadlineDate','priority','deadlineTime']
            x=TaskMate_taskDetails.objects.filter(userName=username).order_by(*orderbyList).values()
            data={'tasks':x}
        except Exception as e:
            print(e)

        return render(request,'homepage.html',data)
    else:
        return redirect('login')

def signUp(request):
    data={}
    if request.method=="POST":
        username=request.POST.get("username")
        email=request.POST.get("email")
        password=request.POST.get("password")
        confirmpassword=request.POST.get("confirmpassword")
        if password!=confirmpassword:
            data["error"]="Passwords do not match"
            return render(request,'signup.html',data)
        else:
            if TaskMate_userDetails.objects.filter(username=username).exists():
                data["error"]="Username already exists"
                return render(request,'signup.html',data)
            elif TaskMate_userDetails.objects.filter(email=email).exists():
                data["error"]="Email already exists"
                return render(request,'signup.html',data)
            else:
                try:
                    user=TaskMate_userDetails(username=username,email=email,password=password)
                    user.save()
                    data["error"]="Account created successfully"
                    return render(request,'signup.html',data)
                except:
                    data["error"]="Something went wrong"
                    return render(request,'signup.html',data)
    else:
        data["error"]=None
        return render(request,'signup.html',data)

def resetPassword(request):
    data={}
    return render(request,'resetPassword.html',data)

def profilePage(request):
    if request.session.has_key('username'):
        if request.method == 'POST':

            profilePic=request.POST.get('photo')
            if profilePic=='':
                x=TaskMate_userDetails.objects.filter(username=request.session['username']).values()
                profilePic=x[0]['profilePic']

            print(profilePic)
            fullName=request.POST.get('fullname')
            mobile=request.POST.get('mobile')
            bio=request.POST.get('bio')

            try:
                TaskMate_userDetails.objects.filter(username=request.session['username']).update(profilePic=profilePic,fullName=fullName,mobileNumber=mobile,bio=bio)
            except Exception as e:
                print(e)

        x=TaskMate_userDetails.objects.filter(username=request.session['username']).values()
        data={'details':x[0]}
        return render(request,'profilePage.html',data)
    else:
        return redirect('login')

def logOut(request):
    del request.session['username']
    return redirect('login')

def delete(request,idd):
    TaskMate_taskDetails.objects.filter(taskId=idd,userName=request.session["username"]).delete()
    return redirect('homepage')