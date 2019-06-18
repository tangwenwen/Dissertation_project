from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from app.models import User_info



def index_teachers(request):
    return render(request,'index_teachers.html')