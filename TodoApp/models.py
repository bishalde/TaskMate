from django.db import models


class TaskMate_userDetails(models.Model):
    username = models.CharField(max_length=30,primary_key=True)
    fullName = models.CharField(max_length=60)
    email = models.EmailField(max_length=254)
    mobileNumber = models.CharField(max_length=15)
    password = models.CharField(max_length=30)
    profilePic = models.ImageField(upload_to='media/',default='/images/user.png')
    bio=models.CharField(max_length=500,default='Hey there! I am using TaskMate.')


class TaskMate_taskDetails(models.Model):
    taskId = models.AutoField(primary_key=True)
    userName = models.CharField(max_length=50)
    deadlineDate = models.CharField(max_length=50)
    deadlineTime = models.CharField(max_length=50)
    priority =models.IntegerField()
    description = models.CharField(max_length=500)
    filename = models.CharField(max_length=300)


