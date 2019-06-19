from django.contrib import admin
from app.models import User_info,Teacher_info,Student_info,Admin_info,student_file,message,broadcast,project
# Register your models here.
admin.site.register(User_info)    #每一张表都要进行注册
admin.site.register(Teacher_info)
admin.site.register(Student_info)
admin.site.register(Admin_info)
admin.site.register(student_file)
admin.site.register(message)
admin.site.register(broadcast)
admin.site.register(project)