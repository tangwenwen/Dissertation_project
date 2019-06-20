from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from app.models import User_info,student_file,project,Student_info,Teacher_info
from app.views import check_login
import os
from django.db.models import Q
from itertools import chain

@check_login
def index_students(request):
    student_file_obj = student_file.objects.filter(email=User_info.objects.get(email=request.session.get('email'))).values()
    student_info_obj = Student_info.objects.filter(student=User_info.objects.get(email=request.session.get('email')))
    #project_obj = project.objects.filter(id=int(student_info_obj[0].project_id))
    student_file_obj_list = list(student_file_obj)
    for i in (student_file_obj_list):
        i['project_name'] = project.objects.filter(id=int(student_info_obj[0].project_id))[0].project_name
        i['project_teacher'] =Teacher_info.objects.filter(Q(project_1=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                                          |Q(project_2=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                                          |Q(project_3=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                                    )[0].teacher_name

    #print(student_file_obj_list)
    if request.method =='GET':
        return render(request,'index_students.html',{'username' : User_info.objects.filter(email=request.session.get('email'))[0].username,
                                                     'student_files':student_file_obj_list,
                                                     'email':User_info.objects.get(email=request.session.get('email')),
                                                     })


#上传文件
def upload_file(request):
    user_email = request.session.get('email')

    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return redirect('/index_students/#table')
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
            return redirect('/index_students/#table')
    else:
        return redirect('/index_students/#table')

#下载文件
def download_file(request,email,student_file_name):
    path = os.path.join('app', 'temp_file', email, student_file_name)
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + student_file_name
    return response

#删除文件
def delete_file(request,email,student_file_name):

    userfile = student_file.objects.get(email=User_info.objects.get(email = email), student_file_name=student_file_name)
    userfile.delete()
    path = os.path.join('app', 'temp_file', email, student_file_name)
    os.remove(path)
    return redirect('/index_students/#table')