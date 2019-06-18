from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from app.models import User_info
from app.views import check_login
import os

@check_login
def index_students(request):
    return render(request,'index_students.html',{'username' : User_info.objects.filter(email=request.session.get('email'))[0].username})


def upload_file(request):
    pass