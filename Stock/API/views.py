from django.shortcuts import render,redirect
import os
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
from .serializers import HistorySerializer
from .models import History
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

userName=''
def getUser(request):
    userName= userName + request.user.username
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

file=open(os.path.join(BASE_DIR,'Stock List.json'),'r')
res=file.read() 
res=json.loads(res)
# Create your views here.
@api_view(['POST'])
def dateFilter(request):
    data=request.data
    if ('from' not in data) or ('to' not in data) or ('symbol' not in data):
        return Response({
            'status':'error',
            'message':'MISSING ONE OR MORE FIELDS'
        })
    # print("2021-01-14">"2021-01-15")
    info=[]
    for i in res:
        if data['from']!='null' and data['to']!='null':
            if i['date']>=data['from'] and i['date']<=data['to']:
                if data['symbol']!='null':
                    if i['symbol']==data['symbol']:
                        info.append(i)
                else:
                    info.append(i)
        else:
            if data['symbol']!='null':
                if i['symbol']==data['symbol']:
                    info.append(i)
            else:
                info.append(i)
            
    return Response({
            'status':'success',
            'data':info
        })

@api_view(['GET'])
def getHistory(request):
    hist=History.objects.all()
    # print(hist)
    # hist=model_to_dict(hist)
    li=[]
    for i in hist:
        li.append(model_to_dict(i))
    return Response({
        'status':'success',
        'info':li
    })

@api_view(["POST"])
def addHistory(request):
    # print(getUser(request))
    data=request.data
    hist=History.objects.create(history=data['history'])
    return Response({
        'status':'success'
    })

def register(request):
    passerror=False
    usererror=False
    # print(request.method)
    alluser=[]
    alluser=User.objects.all()
    if request.method=='POST':
        username=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password1')
        pass2=request.POST.get('password2')
        print(pass1,pass2)
        for i in alluser:
            c=0
            if username==i.username:
                c=c+1
                usererror=True
                break
        if pass1==pass2 and c==0:
            user=User.objects.create_user(username=username,email=email,password=pass1)
            user.save()
            # user=authenticate(request,username=user.username,password=user.password)
            login(request,user)
            return redirect('home')
        elif usererror==False:
            passerror=True
    return render(request,'API/registe.html',{'passerror':passerror,'usererror':usererror})

def auth_login(request):
    print(request.method)
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'username or password is incorrect')
    return render(request,'API/login.html',{})

@login_required
def home(request):
    print(userName)

    return render(request,'index.html',{})

@login_required
def auth_logout(request):
    logout(request)
    return redirect("login")