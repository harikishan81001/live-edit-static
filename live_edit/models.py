from django.contrib.auth.models import User
from django.db import models
import datetime
# Create your models here.
class Records(models.Model):
    check_sum =  models.CharField(max_length=100,unique=True)
    file_name = models.CharField(max_length=250)
    content_diff = models.TextField(null=True,blank=True)
    fetched_dt = models.DateTimeField(default=datetime.datetime.now())
    modified_dt = models.DateTimeField(null=True,blank=True)
    modified_by = models.ForeignKey(User,null=True,blank=True)


