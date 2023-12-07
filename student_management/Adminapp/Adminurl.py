from django.contrib import admin
from django.urls import path
from Adminapp import views
urlpatterns = [
   
    path('HOME',views.First),
    path('H',views.Home),
    path('About',views.About),
    path('',views.MyHomePage,name='Home'),
    path('adminlogin',views.AdminLogin,name='admin'),
    path('UserLogin',views.ULogin,name='user'),
    path('Add',views.Add,name='Add'),
    path('Addition',views.Addition,name='Addition'),
    path('Admin_Login_data',views.Admin_Login_data,name='Admin_Login_data'),
    path('AddSubject',views.AddSubject,name='AddSubject'),
    path('AddStaff',views.AddStaff,name='AddStaff'),
    path('AddSub',views.AddSub,name='AddSub'),
   
]