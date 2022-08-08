from django.contrib import admin
from django.urls import path
from home import views

urlpatterns = [
    path('', views.home, name='home'),
    path('home',views.home,name='home'),
    path('login', views.login, name='login'),
    path('register', views.register, name='register'),
    path('task', views.addtask, name='task'),
    path('tasklist', views.tasklist, name='tasklist'),
    path('about', views.about, name='about'),
    path('logout', views.logout, name='logout'),
    path('activate/<uidb64>/<token>',views.activate,name='activate'),
    path('edit/<int:task_id>',views.edit,name='edit'),
    path('delete/<int:task_id>',views.delete,name='delete'),
]
