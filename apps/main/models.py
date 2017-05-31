from __future__ import unicode_literals
from django.db import models
from ..login.models import User
from django.db.models import Count
from datetime import date
from time import strftime
from model_utils import Choices


class AppointmentManager(models.Manager):
    def add(self, postData):
        print postData
        errors = []
        today = strftime("%Y-%m-%d")
        now = strftime("%H-%M-%S")
        if len(postData['date']) < 1:
            errors.append("You must enter a date that is not a past date.")
        if postData['date'] < str(date.today()):
            errors.append("You must enter a date that is not a past date.")
        if postData['date'] == today and postData['time'] < now:
            errors.append("That time has pasted today. Please enter a future time.")
        if postData['time'] == "":
            errors.append("Please enter a time")
        if len(postData['task']) == 0:
            errors.append("Task cannot be blank. You do not need a calendar to keep track of nothing...")
        if errors:
            return(True, errors)
        else:
            return (False, postData)

    def delete_task(request, postData):
        Appointments.objects.get(id = postData['task_id']).delete()
        return


class Appointments(models.Model):
    user_id = models.ForeignKey(User, related_name='user')
    task = models.CharField(max_length=255)
    time = models.TimeField()
    date = models.DateField()
    status = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = AppointmentManager()
