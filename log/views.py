import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.timezone import now

from programs.apps import ProgramsConfig
from programs.models import Program, ProgramMember, CGC_Member, Student, MscStudent, PhdStudent


def index(request):
    context={
        'programs': Program.objects.all(),
        'cgc_members':CGC_Member.objects.all().order_by('priority'),
    }
    return render(request,'log/index.html', context)

def cgc_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponseRedirect(reverse('log:index'))
    elif user is not None:
        try:
            cgc_member=CGC_Member.objects.get(user=user)
            login(request,user)

            return HttpResponseRedirect(reverse('cgc:cgc_home'))

        except:
            return HttpResponse('Pagina de error de acceso cgc')





def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    program_slug = request.POST['program_slug']
    program = Program.objects.get(slug=program_slug)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponseRedirect(reverse('programs:index', args=[program_slug]))

    elif user is not None:
        if program.type=='phd':
            try:
                try:
                    ProgramMember.objects.filter(user=user, program=program)
                    login(request, user)
                    return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                except:
                    try:
                        Student.objects.get(user=user, program=program)
                        login(request, user)
                        return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                    except:
                        #TODO esta debe ser un template de error
                        return HttpResponse('Error, ni profesor ni estudiante')
            except:
                # TODO esta debe ser un template de error
                return HttpResponse('Error, ni profesor ni estudiante')

        elif program.type == 'msc':
            try:
                try:
                    ProgramMember.objects.filter(user=user, program=program)
                    login(request, user)
                    return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                except:
                    try:
                        MscStudent.objects.filter(user=user, program=program)
                        login(request, user)
                        return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                    except:
                        # TODO esta debe ser un template de error
                        return HttpResponse('Error, ni profesor ni estudiante')
            except:
                # TODO esta debe ser un template de error
                return HttpResponse('Error, ni profesor ni estudiante')

        elif program.type == 'dip':
            return HttpResponse('Hay que implementar este tipo de prrograma')
    else:
        HttpResponseRedirect(reverse('programs:index', args=[program_slug]))
    # TODO si hay error de usuario y contrase;a que redireccione al index del tribunal con un error  especifico

def mylogout(request, program_slug):
    logout(request)
    return HttpResponseRedirect(reverse('programs:index',args=[program_slug]))

def cgc_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('log:index'))

def cgc_member_picture(request, member_id):
    fs = FileSystemStorage()
    # filename = Papers.objects.get(pk=paper_id).file_url +  str(Papers.objects.get(pk=paper_id).file)
    filename = CGC_Member.objects.get(pk=member_id).picture.url
    if fs.exists(filename):
        with fs.open(filename) as img:
            response = HttpResponse(img, content_type='image/jpeg')
            return response
    else:
        return HttpResponse('Error')


