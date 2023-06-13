from django.contrib import admin
from django.urls import path
from TodoApp import views

urlpatterns = [
    path('',views.login , name='login'),
    path('homepage/',views.homepage , name='homepage')
]