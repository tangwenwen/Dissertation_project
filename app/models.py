from django.db import models

# Create your models here

#用户表
class User_info(models.Model):
    username = models.CharField(max_length=30,verbose_name=u"用户名")
    password = models.CharField(max_length=255, verbose_name=u"密码")
    email = models.CharField(max_length=30, verbose_name=u"邮箱")
    create_time = models.DateTimeField(auto_now=True, verbose_name=u"创建时间")
    user_choices = ((1,u'学生'),(2,u"老师"),(3,u"管理员"))
    comment_type = models.IntegerField(choices=user_choices, default=1, verbose_name=u"用户类型")

#学生文件表
class student_file(models.Model):
    email = models.ForeignKey('User_info',on_delete=models.CASCADE, verbose_name=u"邮箱")
    student_file_name = models.CharField(max_length=250, verbose_name=u"学生文件名")
    student_file_size = models.CharField(max_length=30, verbose_name=u"学生文件大小")
    student_upload_time = models.DateTimeField(auto_now=True, verbose_name=u"学生上传时间")
    student_upload_add = models.CharField(max_length=250, verbose_name=u"学生文件地址", default='')

#消息表
class student_message(models.Model):
    pass


#问题表
class student_question(models.Model):
    pass