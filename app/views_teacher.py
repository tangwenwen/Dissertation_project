from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse
from django.conf import settings
from django.db.models import Q

from app.models import User_info, Teacher_info, student_file, Student_info, project, message, broadcast
from app.views import check_login
import os

@check_login
def index_teachers(request):
    teacher_info_obj = Teacher_info.objects.filter(teacher = User_info.objects.get(email=request.session.get('email')))
    teacher_project_list = list()
    student_files = list()
    if teacher_info_obj[0].project_1:
        project_obj1 = project.objects.filter(id=teacher_info_obj[0].project_1.id).values()
        project_list1 = list(project_obj1)

        Student_info_obj = Student_info.objects.filter(project = teacher_info_obj[0].project_1)
        if Student_info_obj:
            student_file_obj = student_file.objects.filter(
                email=User_info.objects.get(email=Student_info_obj[0].student.email)).values()
            student_file_obj_list = list(student_file_obj)
            for i in (student_file_obj_list):
                i['project_name'] = teacher_info_obj[0].project_1.project_name
                i['project_student'] = Student_info_obj[0].student_name
                i['student_email'] = Student_info_obj[0].student.email
            student_files = student_file_obj_list

            for i in (project_list1):
                i['student_name'] = Student_info_obj[0].student_name
                i['student_major'] = Student_info_obj[0].student_major
        teacher_project_list = project_list1

    if teacher_info_obj[0].project_2:
        project_obj2 = project.objects.filter(id = teacher_info_obj[0].project_2.id).values()
        project_list2 = list(project_obj2)

        Student_info_obj2 = Student_info.objects.filter(project=teacher_info_obj[0].project_2)
        if Student_info_obj2:
            student_file_obj2 = student_file.objects.filter(
                email=User_info.objects.get(email=Student_info_obj2[0].student.email)).values()
            student_file_obj_list2 = list(student_file_obj2)
            for i in (student_file_obj_list2):
                i['project_name'] = teacher_info_obj[0].project_2.project_name
                i['project_student'] = Student_info_obj2[0].student_name
                i['student_email'] = Student_info_obj2[0].student.email
            student_files = student_files+student_file_obj_list2

            for i in (project_list2):
                i['student_name'] = Student_info_obj2[0].student_name
                i['student_major'] = Student_info_obj2[0].student_major
        teacher_project_list =teacher_project_list+project_list2

    if teacher_info_obj[0].project_3:
        project_obj3 = project.objects.filter(id=teacher_info_obj[0].project_3.id).values()
        project_list3 = list(project_obj3)

        Student_info_obj3 = Student_info.objects.filter(project=teacher_info_obj[0].project_3)
        if Student_info_obj3:
            student_file_obj3 = student_file.objects.filter(
                email=User_info.objects.get(email=Student_info_obj3[0].student.email)).values()
            student_file_obj_list3 = list(student_file_obj3)
            for i in (student_file_obj_list3):
                i['project_name'] = teacher_info_obj[0].project_1.project_name
                i['project_student'] = Student_info_obj3[0].student_name
                i['student_email'] = Student_info_obj3[0].student.email
            student_files = student_files+student_file_obj_list3

            for i in (project_list3):
                i['student_name'] = Student_info_obj3[0].student_name
                i['student_major'] = Student_info_obj3[0].student_major

        teacher_project_list =teacher_project_list+project_list3

    # 消息面板显示
    messagenum = message.objects.filter(message_reservier=User_info.objects.get(email=request.session.get('email'))).count()
    no_read_messagenum = message.objects.filter(message_flag=1,
                                                    message_reservier=User_info.objects.get(
                                                        email=request.session.get('email'))).count()
    alertnum = broadcast.objects.filter(Q(broadcast_upload_to=3) | Q(broadcast_upload_to=1)).count()

    # 消息messages
    my_messages = message.objects.filter(message_reservier=User_info.objects.get(email=request.session.get('email')))

    return render(request,'index_teachers.html',{'username' : User_info.objects.filter(email=request.session.get('email'))[0].username,
                                                 'teacher_projects':teacher_project_list,
                                                 'student_files':student_files,
                                                 'email':request.session.get('email'),
                                                 'messagenum':messagenum,
                                                 'no_read_messagenum':no_read_messagenum,
                                                 'alertnum':alertnum,
                                                 'my_messages':my_messages,
                                                 })

#删除文件
def delete_file(request,email,student_file_name):

    userfile = student_file.objects.get(email=User_info.objects.get(email = email), student_file_name=student_file_name)
    userfile.delete()
    path = os.path.join('app', 'temp_file', email, student_file_name)
    os.remove(path)
    return redirect('/index_teachers/#table')

#新建项目
def new_project(request):
    teacher_info_obj = Teacher_info.objects.filter(teacher=User_info.objects.get(email=request.session.get('email')))
    if not teacher_info_obj[0].project_1:
        if request.method == 'POST':
            newproject = project(
                project_name=request.POST.get('projectname'),
                project_free=request.POST.get('projectfee'),
                project_image=request.FILES.get('picture'),
                project_enddate=request.POST.get('enddate'),
                project_content=request.POST.get('projectcontent'),
            )
            newproject.save()
            Teacher_info.objects.filter(teacher=User_info.objects.get(email=request.session.get('email'))).update(project_1=newproject)
            return HttpResponse("<script>alert('新建项目成功！');window.history.back();</script>")
    elif not teacher_info_obj[0].project_2:
        if request.method == 'POST':
            newproject = project(
                project_name=request.POST.get('projectname'),
                project_free=request.POST.get('projectfee'),
                project_image=request.FILES.get('picture'),
                project_enddate=request.POST.get('enddate'),
                project_content=request.POST.get('projectcontent'),
            )
            newproject.save()
            Teacher_info.objects.filter(teacher=User_info.objects.get(email=request.session.get('email'))).update(project_2=newproject)
            return HttpResponse("<script>alert('新建项目成功！');window.history.back();</script>")
    elif not teacher_info_obj[0].project_3:
        if request.method == 'POST':
            newproject = project(
                project_name=request.POST.get('projectname'),
                project_free=request.POST.get('projectfee'),
                project_image=request.FILES.get('picture'),
                project_enddate=request.POST.get('enddate'),
                project_content=request.POST.get('projectcontent'),
            )
            newproject.save()
            Teacher_info.objects.filter(teacher=User_info.objects.get(email=request.session.get('email'))).update(project_3=newproject)
            return HttpResponse("<script>alert('新建项目成功！');window.history.back();</script>")
    else:
        return HttpResponse("<script>alert('您当前项目已满，无法再次添加！');window.history.back();</script>")
    return redirect('/index_teachers/#project_manage')

#删除项目
def delete_project(request,email,project_id):
    teacher_info_obj = Teacher_info.objects.filter(teacher=User_info.objects.get(email=email))

    if str(teacher_info_obj[0].project_1.id) == project_id:
        Teacher_info.objects.filter(teacher=User_info.objects.get(email=email)).update(project_1 = None)
    elif str(teacher_info_obj[0].project_2.id) == project_id:
        Teacher_info.objects.filter(teacher=User_info.objects.get(email=email)).update(project_2=None)
    elif str(teacher_info_obj[0].project_3.id) == project_id:
        Teacher_info.objects.filter(teacher=User_info.objects.get(email=email)).update(project_3=None)

    teacher_project = project.objects.get(id = project_id)
    teacher_project.delete()
    return HttpResponse("<script>alert('删除项目成功！');window.history.back();</script>")

#老师回复消息
def teacher_reply(request):
    if request.method =='POST':
        content = request.POST.get('message_content')
        messageid = request.POST.get('messageid')
        messagepublisher = request.POST.get('messagepublisher')
        projectid = request.POST.get('projectid')
        email = request.session.get('email')
        try:
            reply_message = message(message_content = content,      #插入新的消息记录
                                    message_replyto=message.objects.get(id = messageid),
                                    message_reservier=User_info.objects.get(id =messagepublisher),
                                    project=project.objects.get(id = projectid),
                                    message_publisher=User_info.objects.get(email=email),
                                )
            reply_message.save()
            old_message = message.objects.get( id = messageid )      #更改原来的消息回复位
            old_message.message_flag = 2
            old_message.save()
        except:
            raise Exception
    return HttpResponse('ok')

#发起群聊
def teacher_question(request):
    if request.method =='POST':
        content = request.POST.get('question_content')
        projectid = request.POST.get('projectid')

        student_info_obj=Student_info.objects.filter(project=project.objects.get(id=projectid))

        question_message = message(message_content=content,
                                       message_publisher= User_info.objects.get(email=request.session.get('email')),
                                       message_reservier= User_info.objects.get(id = student_info_obj[0].student.id),
                                       project= project.objects.get(id=projectid),)
        question_message.save()


    return HttpResponse('ok')
