from django.contrib import admin
from django.urls import path
from TodoApp import views

urlpatterns = [
    path('',views.login , name='login'),
    path('homepage/',views.homepage , name='homepage'),
    path('signUp/',views.signUp , name='signUp'),
    path('resetPassword/',views.resetPassword , name='resetPassword'),
    path('profilePage/',views.profilePage , name='profilePage'),
    path('logOut/',views.logOut , name='logOut'),
]