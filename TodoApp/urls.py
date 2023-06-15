from django.contrib import admin
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from TodoApp import views

urlpatterns = [
    path('',views.login , name='login'),
    path('homepage/',views.homepage , name='homepage'),
    path('signUp/',views.signUp , name='signUp'),
    path('resetPassword/',views.resetPassword , name='resetPassword'),
    path('profilePage/',views.profilePage , name='profilePage'),
    path('delete/<int:idd>',views.delete,name='delete'),
    path('edit/<int:idd>',views.editTodo,name='editTodo'),
    path('logOut/',views.logOut , name='logOut'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()