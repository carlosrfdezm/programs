from django.shortcuts import render

# Create your views here.
from programs.apps import ProgramsConfig
from programs.models import Program


def index(request):
    context={
        'programs': Program.objects.all(),
    }
    return render(request,'log/index.html', context)