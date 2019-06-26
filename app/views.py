from django.shortcuts import render

# Create your views here.


from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from functools import wraps
from app.models import User_info,Student_info,student_file,project,Teacher_info,broadcast,Admin_info
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from django.db.models import Q

import os


#检验是否登录
def check_login(f):
    @wraps(f)
    def warpfunction(request,*arg,**kwargs):
        if request.session.get('is_login') == '1':
            return f(request,*arg,**kwargs)
        else:
            return HttpResponseRedirect('/login')
    return warpfunction

#登录用户后台代码
def login(request):
    message_error = 'error_login'
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        User = User_info.objects.filter(email=email)
        if User:
            checkPassword = User[0].password
            if check_password(password,checkPassword):
                request.session['is_login'] = '1'  # session expriy = 60*10
                user_type = User[0].comment_type
                if user_type == 3:
                    request.session['email'] = email
                    return HttpResponseRedirect('/')                  #管理员主页
                elif user_type == 2:
                    request.session['email'] = email
                    return HttpResponseRedirect('/index_teachers')             #老师主页
                else :
                    request.session['email'] = email
                    return HttpResponseRedirect('/index_students')              #学生主页
            else :
                return render(request, 'login.html', {"message_error": message_error})
        else:
            return render(request, 'login.html', {"message_error": message_error})

    return render(request, 'login.html')


#退出登录，清除session,回到登录页面
def logout(request):
    request.session.flush()
    return HttpResponseRedirect('/login')

# 主页后台代码
@check_login
def index(request):
    #读取全部文件

    files_obj = student_file.objects.all().values()
    files_obj_list = list(files_obj)
    #for i in (files_obj_list):
       #i['user_name']=User_info.objects.get(email=i['email']).username



    # 所有项目浏览，
    all_project_obj_list = list(project.objects.all().values())
    with_project = ''
    if not all_project_obj_list:
        with_project = 'true'
    for i in all_project_obj_list:
        i['teacher'] = Teacher_info.objects.filter(Q(project_1=i['id'])
                                                   | Q(project_2=i['id'])
                                                   | Q(project_3=i['id'])
                                                   )[0].teacher_name
        i['teachermajor'] = Teacher_info.objects.filter(Q(project_1=i['id'])
                                                        | Q(project_2=i['id'])
                                                        | Q(project_3=i['id'])
                                                        )[0].teacher_major
        i['project_startdate'] = i['project_startdate'].date

    #所有学生
    all_student_obj = Student_info.objects.all()
    all_student_obj_list = list(Student_info.objects.all().values())
    for i in all_student_obj_list:
        i['project_name']=all_student_obj[0].project.project_name
        i['email']=all_student_obj[0].student.email


    #所有教师
    all_teacher_obj = Teacher_info.objects.all()
    all_teacher_obj_list = list(Teacher_info.objects.all().values())
    for i in all_teacher_obj_list:
        i['project1_name'] = all_teacher_obj[0].project_1.project_name
        i['email'] = all_teacher_obj[0].teacher.email
        #i['project2_name'] = all_teacher_obj[0].project_2.project_name
        #i['project3_name'] = all_teacher_obj[0].project_3.project_name





    if request.method == 'GET':
        return render(request, 'index.html',
                      {'username': User_info.objects.filter(email=request.session.get('email'))[0].username,
                       'student_files': files_obj_list,
                       'email': User_info.objects.get(email=request.session.get('email')),
                       'all_projects': all_project_obj_list,
                       'all_students': all_student_obj_list,
                       'all_teachers': all_teacher_obj_list
                       })

#重置密码
def resetpassword(requst,email):
    reset_user=User_info.objects.get(email=email)
    password='123456'
    print(reset_user)
    reset_user.password=make_password(password)
    reset_user.save()
    return render(requst,'index.html')



# 下载文件
def download_file(request, email, student_file_name):
    email=student_file.objects.get(student_file_name=student_file_name)[0].email
    path = os.path.join('app', 'temp_file', email, student_file_name)
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + student_file_name
    return response


# 删除文件
def delete_file(request, email, student_file_name):
    email = student_file.objects.get(student_file_name=student_file_name)[0].email
    userfile = student_file.objects.get(email=User_info.objects.get(email=email), student_file_name=student_file_name)
    userfile.delete()
    path = os.path.join('app', 'temp_file', email, student_file_name)
    os.remove(path)
    return redirect('/index/#table')

#注册用户后台代码
def register(request):
    message = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        confirmpassword = request.POST.get("confirmpassword")
        username = lastname+firstname
        if (not email) or (not password) or (not firstname) or (not lastname) or (not confirmpassword):
            message.append('input_none')
        if password !=confirmpassword:
            message.append('confirm_error')
        if User_info.objects.filter(email=email) :
            message.append('email_exist')
        if not message:
            User = User_info(username=username,password=make_password(password),email=email)
            User.save()
            student = Student_info(student=User)
            student.save()
            message.append('register_successful')
        else:
            return render(request, 'register.html', {"message": message})
        return render(request, 'register.html', {"message": message})

    return render(request,'register.html')

#添加用户
def adduser(request):
    message = []
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        confirmpassword = request.POST.get("confirmpassword")
        role = request.POST.get('role')
        num_role = lambda x: 1 if role == 'student' else 2
        int_role = num_role(role)
        username = lastname+firstname
        if (not email) or (not password) or (not firstname) or (not lastname) or (not confirmpassword):
            message.append('input_none')
        if password !=confirmpassword:
            message.append('confirm_error')
        if User_info.objects.filter(email=email) :
            message.append('email_exist')
        if not message:
            User = User_info(username=username,password=make_password(password),email=email,comment_type=int_role)
            User.save()
            student = Student_info(student=User)
            student.save()
            message.append('register_successful')
        else:
            return render(request, 'index.html', {"message": message})
        return render(request, 'index.html', {"message": message})

    return render(request,'index.html')


#忘记密码后台代码
def forgot_password(request):

    if request.method =="POST":
        email = request.POST.get('email')
        my_sender = '497159777@qq.com'
        my_pass = 'eoptzcyjjdddbheb'
        ret = True
        try:
            msg = MIMEText('我们将与你尽快与你联系','plain','utf-8')
            msg['From'] = formataddr(["From system", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["FK", email])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "这是一封用来更改密码的邮件"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [email, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:
            ret = False
        if ret:
            return render(request, 'forgot_password.html', {"message": 'successful'})
        else:
            return render(request, 'forgot_password.html', {"message": 'unsuccessful'})

    return render(request,'forgot_password.html')

#发送公告
def sendbroadcast(request):
    if request.method =='POST':
        content = request.POST.get('broadcast_content')
        teacherid = request.POST.get('teacherid')
        try:
            the_manger = Admin_info.objects.get(admin=User_info.objects.get(email=request.session.get('email')))
            if the_manger:
                broadcast_message  = broadcast(broadcast_content=content,
                                        manager= the_manger,
                                        broadcast_upload_to= 3
                                     )
                broadcast_message.save()
            else:
                print("debug1")
                return HttpResponse('false')
        except:
            raise Exception

    return HttpResponse('ok')