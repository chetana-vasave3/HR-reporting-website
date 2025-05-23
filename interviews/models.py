from django.db import models

# Create your models here.
# models.py



class Telecaller(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    mail_id = models.EmailField()
    gender = models.CharField(max_length=10)
    experience = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.name} - {self.id}"
    
class Counselor(models.Model):
    name = models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    mail_id = models.EmailField()
    gender = models.CharField(max_length=10)
    experience = models.CharField(max_length=100)
    

    def __str__(self):
        return f"{self.name} - {self.id}"
    

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

class Schedule(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True)  # TEMP
    object_id = models.PositiveIntegerField(null=True)  # TEMP
    candidate = GenericForeignKey('content_type', 'object_id')
    


    scheduled_on = models.DateTimeField()
    remark = models.TextField()
    

    def __str__(self):
        return f"Schedule for {self.candidate} on {self.scheduled_on}"
    
class RolledOutStatus(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    candidate = GenericForeignKey('content_type', 'object_id')

    status = models.CharField(max_length=20)
    remark = models.TextField(blank=True, null=True)
    

    def __str__(self):
        return f"{self.candidate} - {self.status}"