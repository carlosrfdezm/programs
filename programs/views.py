import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.text import slugify

from programs.models import Program, ProgramInitRequirements, PhdStudent, Student, StudentInitRequirement


def index(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug)
    }
    return render(request,'programs/program_index.html', context)

def home(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    if program.type == 'phd':
        context={
            'program': program,
            'requesters': PhdStudent.objects.filter(student__program=program, status='solicitante').__len__(),
            'doctorands': PhdStudent.objects.filter(student__program=program, status='doctorando').__len__(),
            'graduated': PhdStudent.objects.filter(student__program=program, status='graduado').__len__(),

        }
        return render(request, 'programs/phd_home.html', context)
    else:
        pass

# @login_required
def create_student(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST':
        try:
            user= User.objects.get(email=request.POST['student_email'])
        except:
            passwd = program_slug + str(random.randint(1000000, 9999999))
            user = User.objects.create_user(
                slugify(request.POST['student_email'].split('@')[0]),
                request.POST['student_email'],
                '12345678',  # Cambiar despues por contrase;a generada

            )
            user.first_name = request.POST['student_name']
            user.last_name = request.POST['student_surename']
            user.save()

        student = Student(
            user=user,
            program=program,
        )
        student.save()

        new_student=PhdStudent(
            student=student,
            status='solicitante',
        )
        new_student.save()

        for requirement in ProgramInitRequirements.objects.filter(program=program):

            if 'student_requirement_' + str(requirement.id) in request.POST:
                new_student_requirement=StudentInitRequirement(
                    student=student,
                    requirement=requirement,
                    accomplished=True,
                )
                new_student_requirement.save()

            else:
                new_student_requirement = StudentInitRequirement(
                    student=student,
                    requirement=requirement,
                )
                new_student_requirement.save()


        return HttpResponseRedirect(reverse('programs:students_list', args=[program_slug]))
    else:
        context={
            'program':program,
            'init_requirements':ProgramInitRequirements.objects.filter(program=program)
        }
        if Program.objects.get(slug=program_slug).type == 'phd':
            return render(request,'programs/create_phd_student.html', context)
        else:
            return HttpResponse('El programa no es un doctorado')


def students_list(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    context={
        'program': program,
        'students': Student.objects.filter(program=program),
    }
    return render(request, 'programs/students_list.html', context)
