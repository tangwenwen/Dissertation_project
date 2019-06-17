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
