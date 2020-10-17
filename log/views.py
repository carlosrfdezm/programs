import json

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.timezone import now

from programas.settings import INSTITUTION_FULL_NAME, INSTITUTION_SHORT_NAME, INSTITUTION_ADDRESS, INSTITUTION_EMAIL, \
    INSTITUTION_PHONE
from programs.apps import ProgramsConfig
from programs.models import Program, ProgramMember, CGC_Member, Student, MscStudent, PhdStudent, DipStudent, \
    PostgMember


def index(request):
    context={
        'programs': Program.objects.all().order_by('-type'),
        'cgc_members':CGC_Member.objects.all().order_by('priority'),
        'institution_full_name': INSTITUTION_FULL_NAME,
        'institution_short_name': INSTITUTION_SHORT_NAME,
        'institution_address': INSTITUTION_ADDRESS,
        'institution_email': INSTITUTION_EMAIL,
        'institution_phone': INSTITUTION_PHONE,
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

        except CGC_Member.DoesNotExist:
            return HttpResponse('Pagina de error de acceso cgc')

def postg_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponseRedirect(reverse('log:index'))
    elif user is not None:
        try:
            postg_member=PostgMember.objects.get(user=user)
            login(request,user)

            return HttpResponseRedirect(reverse('postg:postg_home'))

        except PostgMember.DoesNotExist:
            return HttpResponse('Pagina de error de acceso postg')





def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    program_slug = request.POST['program_slug']
    program = Program.objects.get(slug=program_slug)
    user = authenticate(request, username=username, password=password)
    if user is None:
        return render(request, 'log/login_error.html', {'program':program,'error_message':
                                                            'El nombre de usuario introducido no existe o la contraseña es incorrecta'})


    else:
        try:
            member = ProgramMember.objects.get(user=user, program=program)
            login(request, user)
            return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
        except ProgramMember.DoesNotExist:
            if program.type=='phd':
                try:
                    student=Student.objects.get(user=user, program=program)
                    login(request, user)
                    return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                except Student.DoesNotExist:
                    context = {
                        'error_message':'Usted no es profesor ni estudiante de este programa doctoral',
                        'program':program,
                    }
                    #TODO esta debe ser un template de error
                    return render(request, 'log/login_error.html',context)


            elif program.type == 'msc':
                try:
                    student=MscStudent.objects.get(user=user, program=program)
                    login(request, user)
                    return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                except MscStudent.DoesNotExist:
                    context = {
                        'error_message': 'Usted no es profesor ni estudiante de este programa de maestría',
                        'program': program,
                    }
                    return render(request, 'log/login_error.html', context)

            elif program.type == 'dip':
                try:
                    student = DipStudent.objects.get(user=user, program=program)
                    login(request, user)
                    return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
                except DipStudent.DoesNotExist:
                    context = {
                        'error_message': 'Usted no es profesor ni estudiante de este diplomado',
                        'program': program,
                    }
                    return render(request, 'log/login_error.html', context)

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


