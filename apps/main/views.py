from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import Appointments
from ..login.models import User
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db.models import Count
from datetime import datetime, timedelta, time, date
from time import strftime



# Features required:
#
# Login and Registration with validations. Validation errors should appear on the page.
# Display appointments on two tables (current and future-dated appointments)
# Edit and Delete record for an appointment.
# Add an appointment for current and future dates. Displays error when the date is before the current date

#Views needed
# 1. render index.html - DONE
# 2. show items on index.html
# 3. render add items.html -
# 4. add items to wishlist models
# 5. render details.html -
# 6. show individuals who have the item on thier lists
# 7. allow user to add items to thier lists... Many-to-Many challege?

def index(request): # 1. render index.html
    if "id" not in request.session:
        return redirect("login:index")
    else:
        now = datetime.now()
        context ={
        'my_appt': Appointments.objects.filter(user_id=request.session['id']),
        'appt': Appointments.objects.all(),
        'date': datetime.now().date(),
        'today_appt': Appointments.objects.filter(user_id=request.session['id']).order_by('date').order_by('time'),
        'future_appt': Appointments.objects.filter(user_id=request.session['id']).exclude(date=now).order_by('date').order_by('time')
        }
        return render(request, "main/index.html", context)

def add(request):
    appt = Appointments.objects.add(request.POST)
    user = User.objects.get(id=request.session['id'])

    if appt[0] == False:
        new_appt = Appointments.objects.create(user_id=user, task=request.POST['task'], date=request.POST['date'], time=request.POST['time'], status=request.POST['status'])
        new_appt.save()
        print new_appt
        return redirect(reverse ('main:index'))
    else:
        errors = appt[1]
        for error in errors:
            messages.error(request, error)
        return redirect(reverse ('main:index'))

def edit(request, id):
    if "id" not in request.session:
        return redirect("login:index")
    context = {
        'appt' : Appointments.objects.get(id=id)
    }
    return render(request, 'main/edit.html', context)

def update(request, id):
    appt = Appointments.objects.add(request.POST)
    logged_in = User.objects.get(id=request.session['id'])

    if appt[0] == False:
        appt = Appointments.objects.get(id=id)
        appt.task = request.POST['task']
        appt.status = request.POST['status']
        appt.date = request.POST['date']
        appt.time = request.POST['time']
        appt.save()
        return redirect('main:index')
    else:
        errors = appt[1]
        for error in errors:
            messages.error(request, error)
        return redirect(reverse ('main:edit', kwargs={'id':id}))

def delete(request, id):
    delete = {
    'task_id':id
    }
    Appointments.objects.delete_task(delete)
    return redirect('main:index')
