from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from programs.models import Program, ProgramInitRequirements


def index(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug)
    }
    return render(request,'programs/program_index.html', context)

def home(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug)
    }
    return render(request, 'programs/phd_home.html', context)

# @login_required
def create_student(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST':
        pass
    else:
        context={
            'program':program,
            'init_requirements':ProgramInitRequirements.objects.filter(program=program)
        }
        if Program.objects.get(slug=program_slug).type == 'phd':
            return render(request,'programs/create_phd_student.html', context)
