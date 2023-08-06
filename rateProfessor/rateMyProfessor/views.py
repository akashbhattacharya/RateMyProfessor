from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import *


# Create your views here.
@csrf_exempt
def HandleRegister(request):
    if request.method == 'POST':
        un = request.POST['username']
        em = request.POST['email']
        pw = request.POST['password']
        user = User.objects.create_user(username=un, email=em, password=pw)
        user.save()
        return HttpResponse("User has been registered")
    else:
        return HttpResponse("Only POST methods allowed")


@csrf_exempt
def HandleLogin(request):
    if request.method == 'POST':
        un = request.POST['username']
        pw = request.POST['password']
        user = authenticate(request, username=un, password=pw)
    if user is not None:
        if user.is_active:
            login(request, user)
            if user.is_authenticated:
                print('Successfully logged in')
            return HttpResponse('Successfully logged in')
        else:
            return HttpResponse('Account is disabled')
    else:
        return HttpResponse('Invalid login details')


@csrf_exempt
def HandleLogout(request):
    logout(request)
    return HttpResponse("Logout Successful")


def HandleList(request):
    if request.method != 'GET':
        return HttpResponse("Only GET requests allowed")

    moduleInstances = ModuleInstance.objects.all()
    moduleList = []
    for instance in moduleInstances:
        item = {'Module Name': instance.module.name, 'Module ID': instance.module.id, 'Year': instance.year,
                'Semester': instance.semester,
                'Professors': instance.professor.all().values()
                }
        moduleList.append(item)
        moduleList.append('\n')
    # payload = {'List of Modules':moduleList}
    httpResponse = HttpResponse(moduleList)
    httpResponse.status_code = 200
    return httpResponse


def HandleView(request):
    if request.method != 'GET':
        return HttpResponse("Only GET methods allowed")
    professorList = []
    for p in Professor.objects.all():
        avgRating = 0
        count = 0

        for r in Ratings.objects.all():
            if p == r.professor:
                avgRating += r.rating
                count += 1

        if count > 0:
            avgRating = round(avgRating / count)
        item = {'Name': p.name, 'Rating': avgRating}
        professorList.append(item)
        professorList.append('\n')

    return HttpResponse(professorList)


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
            # response = {'Module ID- ': mid, 'Professor ID- ': pid, 'Average Rating- ': avgRating}
            return HttpResponse("The average rating of professor {} for module {} is {}".format(pid, mid, avgRating))
    else:
        return HttpResponse("Only POST requests allowed")


@csrf_exempt
def HandleRate(request):
    if request.method == 'POST':
        mid = request.POST['mid']
        pid = request.POST['pid']
        year = request.POST['year']
        sem = request.POST['sem']
        rate = request.POST['rate']
        try:
            instance = ModuleInstance.objects.get(module=mid, year=year, semester=sem, professor=pid)
            if int(rate) > 5 or int(rate) < 1:
                return HttpResponse('Your rating must be between 1-5 ')
            else:
                Ratings.objects.create(moduleInstance=instance, professor=Professor.objects.get(id=pid),
                                       rating=int(rate))
                return HttpResponse("Rating saved")
        except ModuleInstance.DoesNotExist:
            return HttpResponse('Module Not Found')
    else:
        return HttpResponse("Only POST requests allowed")



