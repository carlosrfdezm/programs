from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from programs.models import Program


def index(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug)
    }
    return render(request,'programs/index.html', context)

def home(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug)
    }
    return render(request, 'programs/phd_home.html', context)
