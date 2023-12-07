from django.db import models

# Create your models here.
class Subject_Model(models.Model):
    sid=models.AutoField(primary_key=True)
    s_name=models.CharField(max_length=250)
    
    status=models.CharField(default="Available",editable=False,max_length=20)
    class Meta:
        db_table='subject'
class StaffModel(models.Model):
    id=models.AutoField(primary_key=True)
    staff_name=models.CharField(max_length=250)
    mobile=models.CharField(max_length=10)
    mail=models.CharField(max_length=250)
    experience=models.CharField(max_length=250)
    staff_status=models.CharField(default="Available",editable=False,max_length=20)
    class Meta:
        db_table='staff'
