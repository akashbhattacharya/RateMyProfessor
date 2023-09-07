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
    if User.objects.filter(email=em).exists():
        messages.error(request, 'This email already exists')
        return redirect('http://127.0.0.1:8000/')
    if User.objects.filter(username=un).exists():
        messages.error(request, 'This username is taken')
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

def HandlePrevious(request):
    previousRatings = []
    ratings = Ratings.objects.filter(user=User.objects.get(username=request.user))
    for r in ratings:
        item = {'Module_Name': r.moduleInstance.module.name, 'Module_ID': r.moduleInstance.id, 'Year': r.moduleInstance.year,
                'Semester': r.moduleInstance.semester,
                'Professor': r.professor.name, 'Rating': r.rating
                }
        previousRatings.append(item)
    return previousRatings

@login_required(login_url='http://127.0.0.1:8000/')
@csrf_exempt
def HandleRate(request):
    if request.method != 'POST':
        return HttpResponse("Please log-in first")
    mid = request.POST['mid']
    rate = request.POST['rate']
    instance = ModuleInstance.objects.get(id=int(mid))
    if not Ratings.objects.filter(moduleInstance=instance, user=User.objects.get(username=request.user)).exists():
        Ratings.objects.create(moduleInstance=instance, professor=Professor.objects.get(id=instance.professor.id),
                               rating=int(rate), user=User.objects.get(username=request.user))
    else:
        update = Ratings.objects.get(moduleInstance=instance, user=User.objects.get(username=request.user))
        update.rating = rate
        update.save()
    return redirect('/menu')


def HandleHome(request):
    return render(request, 'home.html')


@login_required(login_url='http://127.0.0.1:8000/')
def HandleMenu(request):
    data = {
        'view': HandleView(),
        'list': HandleList(),
        'previous': HandlePrevious(request)
    }
    return render(request, 'menu.html', data)
