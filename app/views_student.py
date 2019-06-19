from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from app.models import User_info,student_file
from app.views import check_login
import os

@check_login
def index_students(request):
    return render(request,'index_students.html',{'username' : User_info.objects.filter(email=request.session.get('email'))[0].username})


def upload_file(request):
    user_email = request.session.get('email')
    User =  User_info.objects.filter(email=user_email)
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return redirect('/index_students')
        else:
            isExists = os.path.exists('./app/temp_file/%s' % user_email)
            if not isExists:
                os.makedirs('./app/temp_file/%s' % user_email)
            file_path = os.path.join('app', 'temp_file', user_email, file_obj.name)
            with open(file_path, 'wb+') as f:
                for chunk in file_obj.chunks():
                    f.write(chunk)
            fsize = os.path.getsize(file_path)
            fobj = User_info.objects.get(email=user_email)
            user_file_obj = student_file(email=fobj, student_file_name=file_obj.name, student_file_size=fsize,student_upload_add=file_path)
            user_file_obj.save()
            return redirect('/index_students')
    else:
        return redirect('/index_students')
