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

from django.conf.urls.static import static
from django.conf import settings
from app import views,views_student,views_teacher


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index),          #管理员主页路由
    path('index_teachers/', views_teacher.index_teachers),          #老师端主页路由
    path('index_students/', views_student.index_students),          #学生端主页路由
    path('register/', views.register),   #注册路由
    path('login/', views.login),       #登录路由
    path('forgot_password/', views.forgot_password),        #忘记密码路由
    path('logout/',views.logout),         #退出出登录路由
    path('upload_file/',views_student.upload_file),   #学生删除文件
    path('download_file/<str:email>/<str:student_file_name>/' ,views_student.download_file,name="download_file"),#学生下载文件
    path('delete_file/<str:email>/<str:student_file_name>/' ,views_student.delete_file,name="delete_file"),  #学生删除文件
    path('delete_file_teacher/<str:email>/<str:student_file_name>/' ,views_teacher.delete_file,name="delete_file_teacher"),  #老师删除文件
    path('index_students/alter_personal_info/<str:email>/' ,views_student.alter_personal_info,name="alter_personal_info"), #学生修改个人资料
    path('index_students/alter_personal_psd/<str:email>/' ,views_student.alter_personal_psd,name="alter_personal_psd"), #学生修改个人密码
    path('index_students/select_project/<str:email>/<int:project_id>/' ,views_student.select_project,name="select_project"), #学生选择项目
    path('index_students/reply/', views_student.reply,name="reply"),  # 学生回复消息
    path('newproject/',views_teacher.new_project),   #老师新建项目
    path('index_students/question/', views_student.question,name="question"),  # 学生向指导老师提问
    path('adduser/',views.adduser), #添加用户
    path('sendbroadcast/',views.sendbroadcast), #发布公告
    #path('resetpassword/',views.resetpassword,name="resetpassword"),
    path('index_students/download_teacher_file/<str:teacheremail>/<str:filename>', views_student.download_teacher_file,name="download_teacher_file"),  # 学生端指导老师的文件下载
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
