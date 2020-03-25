from django.contrib.auth import authenticate, login, logout
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from django.urls import reverse

from programs.apps import ProgramsConfig
from programs.models import Program, ProgramMember, CGC_Member


def index(request):
    context={
        'programs': Program.objects.all(),
    }
    return render(request,'log/index.html', context)

def mylogin(request):
    username = request.POST['username']
    password = request.POST['password']
    program_slug = request.POST['program_slug']
    user = authenticate(request, username=username, password=password)
    if user is None:
        return HttpResponseRedirect(reverse('programs:index', args=[program_slug]))

    elif user is not None:
        try:
            ProgramMember.objects.get(user=user, program=Program.objects.get(slug=program_slug))
            login(request, user)
            return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
        except:
            if user.is_superuser:
                login(request, user)
                return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))
            else:
                try:
                    login(request, user)
                    user_program = ProgramMember.objects.get(user=user).program
                    return HttpResponseRedirect(reverse('programs:home', args=[user_program.slug]))
                except:
                    pass
                # return HttpResponseRedirect(reverse('courts:auth_error', args=[court_slug, '2' ]))
                     # TODO si el usuario no es miembro de este tribunal que redireccione al index del tribunal con un error  especifico
    else:
       HttpResponseRedirect(reverse('programs:index', args=[program_slug]))
    # TODO si hay error de usuario y contrase;a que redireccione al index del tribunal con un error  especifico

def mylogout(request, program_slug):
    logout(request)
    return HttpResponseRedirect(reverse('programs:index',args=[program_slug]))

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