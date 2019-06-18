from django.db import models

# Create your models here

#用户表
class User_info(models.Model):
    username = models.CharField(max_length=30,verbose_name=u"用户名")
    password = models.CharField(max_length=30, verbose_name=u"密码")
    email = models.CharField(max_length=30, verbose_name=u"邮箱")
    create_time = models.DateTimeField(auto_now=True, verbose_name=u"创建时间")
    user_choices = ((1,u'学生'),(2,u"老师"),(3,u"管理员"))
    comment_type = models.IntegerField(choices=user_choices, default=1, verbose_name=u"用户类型")
