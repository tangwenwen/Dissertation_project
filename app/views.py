from django.shortcuts import render

# Create your views here.


from django.contrib.auth.hashers import make_password,check_password
from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from functools import wraps
from app.models import User_info,Student_info,student_file,project,Teacher_info
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

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
    email = request.session.get('email')
    Userobj = User_info.objects.filter(email=email)
    if Userobj:
        return render(request, 'index.html',{'username': User_info.objects.filter(email=request.session.get('email'))[0].username})
    else:
        return render(request, 'index.html')
    student_file_obj = student_file.objects.filter(email=User_info.objects.get(email=request.session.get('email'))).values()
    student_info_obj = Student_info.objects.filter(student=User_info.objects.get(email=request.session.get('email')))
    # project_obj = project.objects.filter(id=int(student_info_obj[0].project_id))
    student_file_obj_list = list(student_file_obj)
    for i in (student_file_obj_list):
        i['project_name'] = project.objects.filter(id=int(student_info_obj[0].project_id))[0].project_name
        i['project_teacher'] = Teacher_info.objects.filter(Q(project_1=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                    | Q(project_2=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                    | Q(project_3=project.objects.filter(id=int(student_info_obj[0].project_id))[0].id)
                                    )[0].teacher_name

    # print(student_file_obj_list)
    if request.method == 'GET':
        return render(request, 'index_students.html',
                      {'username': User_info.objects.filter(email=request.session.get('email'))[0].username,
                       'student_files': student_file_obj_list,
                       'email': User_info.objects.get(email=request.session.get('email')),
                       })


# 上传文件
def upload_file(request):
    user_email = request.session.get('email')

    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj is None:
            return redirect('/index/#table')
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
            user_file_obj = student_file(email=fobj, student_file_name=file_obj.name, student_file_size=fsize,
                                         student_upload_add=file_path)
            user_file_obj.save()
            return redirect('/index/#table')
    else:
        return redirect('/index_students/#table')


# 下载文件
def download_file(request, email, student_file_name):
    path = os.path.join('app', 'temp_file', email, student_file_name)
    file = open(path, 'rb')
    response = HttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename=' + student_file_name
    return response


# 删除文件
def delete_file(request, email, student_file_name):
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
