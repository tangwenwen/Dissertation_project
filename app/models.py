from django.db import models

# Create your models here

#用户表
class User_info(models.Model):
    username = models.CharField(max_length=30,verbose_name=u"用户名",default='')
    password = models.CharField(max_length=255, verbose_name=u"密码",default='')
    email = models.CharField(max_length=30, verbose_name=u"邮箱")
    create_time = models.DateTimeField(auto_now=True, verbose_name=u"创建时间")
    user_choices = ((1,u'学生'),(2,u"老师"),(3,u"管理员"))
    comment_type = models.IntegerField(choices=user_choices, default=1, verbose_name=u"用户类型")
    def __str__(self):
        return self.username

#老师表
class Teacher_info(models.Model):
    teacher = models.OneToOneField(to = 'User_info',on_delete=models.CASCADE, verbose_name=u"老师",default='')
    teacher_name = models.CharField(max_length=255, verbose_name=u"教师姓名",default='')
    teacher_school = models.CharField(max_length=255, verbose_name=u"教师学校",default='')
    teacher_major = models.CharField(max_length=255, verbose_name=u"教师专业",default='')
    project_1 = models.OneToOneField(to='project',related_name='project_1', on_delete=models.CASCADE, verbose_name=u"老师项目项目一" ,null=True,blank=True)
    project_2 = models.OneToOneField(to='project', related_name='project_2',on_delete=models.CASCADE, verbose_name=u"老师项目项目二" ,null=True,blank=True)
    project_3 = models.OneToOneField(to='project', related_name='project_3',on_delete=models.CASCADE, verbose_name=u"老师项目项目三" ,null=True,blank=True)
    def __str__(self):
        return self.teacher_name

#学生表
class Student_info(models.Model):
    student = models.OneToOneField(to ='User_info',on_delete=models.CASCADE, verbose_name=u"学生")
    student_sex_choices = ((1, u'男'), (2, u"女"))
    student_sex = models.IntegerField(choices=student_sex_choices, default=1, verbose_name=u"学生性别")
    student_major = models.CharField(max_length=255, verbose_name=u"学生专业",default='')
    student_name = models.CharField(max_length=255, verbose_name=u"学生姓名",default='')
    student_school = models.CharField(max_length=255, verbose_name=u"学生学校",default='')
    student_class = models.CharField(max_length=255, verbose_name=u"学生所在班级",default='')
    project = models.OneToOneField(to='project',on_delete=models.CASCADE, verbose_name=u"学生项目"  ,null=True,blank=True)
    def __str__(self):
        return self.student_name

#g管理员表
class Admin_info(models.Model):
    admin = models.OneToOneField(to='User_info',on_delete=models.CASCADE, verbose_name=u"管理员" )
    admin_name = models.CharField(max_length=255, verbose_name=u"管理员名称",default='')
    def __str__(self):
        return self.admin_name

#学生文件表
class student_file(models.Model):
    email = models.ForeignKey(to ='User_info',on_delete=models.CASCADE, verbose_name=u"邮箱" ,default='')
    student_file_name = models.CharField(max_length=250, verbose_name=u"学生文件名",default='')
    student_file_size = models.CharField(max_length=30, verbose_name=u"学生文件大小",default='')
    student_upload_time = models.DateTimeField(auto_now=True, verbose_name=u"学生上传时间")
    student_upload_add = models.CharField(max_length=250, verbose_name=u"学生文件地址", default='')
    student_file_choices = ((1, u'未查阅'), (2, u"已查阅"))
    student_file_flag = models.IntegerField(choices=student_file_choices, default=1, verbose_name=u"文件是否被老师查阅")
    def __str__(self):
        return self.student_file_name

#消息表
class message(models.Model):
    project = models.ForeignKey('project',on_delete=models.CASCADE, verbose_name=u"何项目的消息" ,default='')
    message_content = models.TextField(verbose_name=u"消息内容",default='')
    message_replyto = models.ForeignKey('self',related_name="子消息",blank=True,null=True,verbose_name=u"父消息",on_delete=models.CASCADE)
    message_upload_time = models.DateTimeField(auto_now=True, verbose_name=u"消息公告时间")
    message_publisher = models.ForeignKey('User_info', related_name='publisher', on_delete=models.CASCADE, verbose_name=u"发布消息的人",default='')
    message_reservier = models.ForeignKey('User_info', related_name='reservier' , on_delete=models.CASCADE, verbose_name=u"接收消息的人",default='')
    message_choices = ((1, u'未查看'), (2, u"已查看"))
    message_flag = models.IntegerField(choices=message_choices, default=1, verbose_name=u"消息是否被查看")
    def __str__(self):
        return self.message_publisher.username
    def clean(self):
        if self.message_replyto:        #如果有回复位，则置flag为已查看
            self.message_flag = 2

#公告表
class broadcast(models.Model):
    manager = models.ForeignKey('Admin_info',on_delete=models.CASCADE, verbose_name=u"发布公告的管理员" ,default='')
    broadcast_upload_time = models.DateTimeField(auto_now=True, verbose_name=u"发布公告时间")
    broadcast_title = models.CharField(max_length=250, verbose_name=u"公告标题",default='')
    broadcast_content = models.TextField(verbose_name=u"公告内容",default='')
    broadcast_choices = ((1, u'学生'), (2, u"老师"),(3, u"所有广播"))
    broadcast_upload_to = models.IntegerField(choices=broadcast_choices, default=1, verbose_name=u"向何用户发布")
    def __str__(self):
        return self.broadcast_title

#项目表
class project(models.Model):
    project_name = models.CharField(max_length=250, verbose_name=u"项目名称",default='')
    project_free = models.CharField(max_length=250, verbose_name=u"项目经费",default='')
    project_startdate = models.DateTimeField(auto_now=True, verbose_name=u"项目开始时间")
    project_enddate = models.DateTimeField(auto_now=False, verbose_name=u"项目结束时间")
    project_choices = ((1,u'未结题'),(2,u"已结题"))
    project_project_isfinished = models.IntegerField(choices=project_choices, default=1, verbose_name=u"项目当前状态")
    project_image = models.ImageField(blank=True,null=True,verbose_name=u"项目介绍图片")
    project_content = models.TextField(verbose_name=u"项目介绍", default='')
    project_choices = ((1, u'未被选择'), (2, u"已被选择"))
    project_flag = models.IntegerField(choices=project_choices, default=1, verbose_name=u"项目是否被选择")
    def __str__(self):
        return self.project_name