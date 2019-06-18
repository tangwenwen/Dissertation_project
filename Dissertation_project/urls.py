"""Dissertation_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views,views_student,views_teacher


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),          #管理员主页路由
    path('index_teachers/', views_teacher.index_teachers),          #老师端主页路由
    path('index_students/', views_student.index_students),          #学生端主页路由
    path('register/', views.register),   #注册路由
    path('login/', views.login),       #登录路由
    path('forgot_password/', views.forgot_password),        #忘记密码路由
    path('logout/',views.logout),         #推出登录路由

]
