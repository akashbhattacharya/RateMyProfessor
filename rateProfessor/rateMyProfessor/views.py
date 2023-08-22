from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *


@csrf_exempt
def HandleRegister(request):
    if request.method != 'POST':
        return redirect('http://127.0.0.1:8000/')
    un = request.POST['username']
    em = request.POST['email']
    pw = request.POST['password']
    if User.objects.filter(email=em).exists() or User.objects.filter(username=un).exists():
        messages.error(request, 'Username or email already exists')
        return redirect('http://127.0.0.1:8000/')
    user = User.objects.create_user(username=un, email=em, password=pw)
    user.save()
    messages.success(request, 'User successfully registered')
    return redirect('http://127.0.0.1:8000/')


@csrf_exempt
def HandleLogin(request):
    if request.method != 'POST':
        return redirect('http://127.0.0.1:8000/')
    un = request.POST['username']
    pw = request.POST['password']
    user = authenticate(request, username=un, password=pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.is_authenticated:
                return redirect('/menu')
        else:
            return HttpResponse('Account is disabled')
    else:
        messages.warning(request, 'Invalid login credentials, please try again')
        return redirect('http://127.0.0.1:8000/')


@csrf_exempt
def HandleLogout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')


def HandleList():
    moduleInstances = ModuleInstance.objects.all()
    moduleList = []
    for instance in moduleInstances:
        item = {'Module_Name': instance.module.name, 'Module_ID': instance.id, 'Year': instance.year,
                'Semester': instance.semester,
                'Professor': instance.professor.name
                }
        moduleList.append(item)
    return moduleList


def HandleView():
    professorList = []
    for p in Professor.objects.all():
        avgRating = 0
        count = 0

        for r in Ratings.objects.all():
            if p == r.professor:
                avgRating += r.rating
                count += 1

        if count > 0:
            avgRating = round((avgRating / count), 1)
        item = {'Name': p.name, 'Rating': avgRating, 'ID': p.id}
        professorList.append(item)
    return professorList


@csrf_exempt
def HandleAverage(request):
    if request.method == 'POST':
        mid = request.POST['mid']
        pid = request.POST['pid']
        check = False
        avgRating = 0
        count = 0
        for r in Ratings.objects.all():
            try:
                if (r.professor == Professor.objects.get(id=pid) and r.moduleInstance.module == Module.objects.get(
                        id=mid)):
                    check = True
                    avgRating += int(r.rating)
                    count += 1
            except Module.DoesNotExist:
                return HttpResponse('Module Not Found')
            except Professor.DoesNotExist:
                return HttpResponse('Professor Not Found')
        if check is False:
            return HttpResponse("Could not find rating")
        else:
            avgRating = round(avgRating / count)
            return HttpResponse("The average rating of professor {} for module {} is {}".format(pid, mid, avgRating))
    else:
        return HttpResponse("Only POST requests allowed")


@csrf_exempt
def HandleRate(request):
    if request.method != 'POST':
        return HttpResponse("Please log-in first")
    mid = request.POST['mid']
    rate = request.POST['rate']
    instance = ModuleInstance.objects.get(id=int(mid))
    Ratings.objects.create(moduleInstance=instance, professor=Professor.objects.get(id=instance.professor.id),
                           rating=int(rate))
    return redirect('/menu')


def HandleHome(request):
    return render(request, 'home.html')


@login_required(login_url='http://127.0.0.1:8000/')
def HandleMenu(request):
    data = {
        'view': HandleView(),
        'list': HandleList()
    }
    return render(request, 'menu.html', data)
