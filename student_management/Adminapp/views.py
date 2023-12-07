from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from Adminapp.forms import subject_form
from Adminapp.models import Subject_Model,StaffModel

from rest_framework import viewsets
#from Adminapp.serializers import StaffModelSerializer

""" class StaffModelViewSet(viewsets.ModelViewSet):
    queryset = StaffModel.objects.all()
    serializer_class = StaffModelSerializer """

# Create your views here.
def First(request):
    return HttpResponse("<h1>Welcome to Facebook</h1>")
def Home(request):
    return HttpResponse("Facebook Home page ")
def About(request):
    return HttpResponse("Facebook About Page")
def MyHomePage(request):
    return render(request,"Home.html")
def AdminLogin(request):
    return render(request,"AdminLogin.html")
def Admin_Login_data (request):
    name=request.POST["uname"]
    pw=request.POST["pw"]
    if(name!="admin" or pw!="1234"):
        messages.warning(request,"Invalid Credentials")
        return render(request,"AdminLogin.html")
    else:
        messages.success(request,"Login success")
        return render(request,"AdminHome.html")
def AddStaff(request):
    return render(request,"AddStaff.html")
def AddSubject(request):
    a1=subject_form(request.GET)	
    return render(request,"AddSubject.html",{"f":a1})
    #return render(request,"AddSubject.html")
def AddSub(request):
    a1=subject_form(request.GET)
    if(a1.is_valid()):
        a1.save()
        messages.success(request,"Registered Successfully")	
    return render(request,"AddSubject.html",{"f":a1})
def ULogin(request):
    return render(request,"UserLogin.html")
def Add(request):
    return render(request,"Addition.html")
def Addition(request):
    A=int(request.POST['value1'])
    B=request.POST['value2']
    option=request.POST['opt']
    if(option=="add"):
        c=A+int(B)
        print(c)
    elif(option=="sub"):
        c=A-int(B)
        print(c)
    #return render(request,"Addition.html",{'ans':c})
    return render(request,"Result.html",{'ans':c})