from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.conf import settings

from app.models import User_info, Teacher_info, student_file, Student_info, project
from app.views import check_login
import os

@check_login
def index_teachers(request):
    teacher_info_obj = Teacher_info.objects.filter(teacher = User_info.objects.get(email=request.session.get('email')))
    teacher_project_list = list()
    if teacher_info_obj[0].project_1:
        teacher_project_list.append(teacher_info_obj[0].project_1)
        Student_info_obj = Student_info.objects.filter(project = teacher_info_obj[0].project_1)
        student_file_obj = student_file.objects.filter(
            email=User_info.objects.get(email=Student_info_obj[0].student.email)).values()
        student_file_obj_list = list(student_file_obj)
        for i in (student_file_obj_list):
            i['project_name'] = teacher_info_obj[0].project_1.project_name
            i['project_student'] = Student_info_obj[0].student_name

    if teacher_info_obj[0].project_2:
        teacher_project_list.append(teacher_info_obj[0].project_2)

    if teacher_info_obj[0].project_3:
        teacher_project_list.append(teacher_info_obj[0].project_3)


    return render(request,'index_teachers.html',{'username' : User_info.objects.filter(email=request.session.get('email'))[0].username,
                                                 'teacher_projects':teacher_project_list,
                                                 'student_files':student_file_obj_list,
                                                 'email':Student_info_obj[0].student.email})

#删除文件
def delete_file(request,email,student_file_name):

    userfile = student_file.objects.get(email=User_info.objects.get(email = email), student_file_name=student_file_name)
    userfile.delete()
    path = os.path.join('app', 'temp_file', email, student_file_name)
    os.remove(path)
    return redirect('/index_teachers/#table')

def new_project(request):
    print(request.FILES.get('picture'))
    if request.method == 'POST':
        newproject = project(
            project_name=request.POST.get('projectname'),
            project_free = request.POST.get('projectfee'),
            project_image=request.FILES.get('picture'),
            project_enddate = request.POST.get('enddate'),
            project_content='11111',
        )
        newproject.save()
    return redirect('/index_teachers/#project_manage')
