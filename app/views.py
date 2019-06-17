from django.shortcuts import render

# Create your views here.



from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from functools import wraps

import os

# 主页后台代码
def index(request):
    return render(request,'index.html')

#注册用户后台代码
def register(request):
    return render(request,'register.html')


#登录用户后台代码
def login(request):
    return render(request,'login.html')


#忘记密码后台代码
def forgot_password(request):
    return render(request,'forgot-password.html')
