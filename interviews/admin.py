from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Telecaller,Counselor,Schedule,RolledOutStatus

@admin.register(Telecaller)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'mail_id', 'gender', 'experience', 'id')

@admin.register(Counselor)
class CounselorAdmin(admin.ModelAdmin):
    list_display = ('name', 'contact', 'mail_id', 'gender', 'experience', 'id')

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'scheduled_on', 'remark')
    
@admin.register(RolledOutStatus)
class RolledOutStatusAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'status', 'remark')