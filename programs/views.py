import random

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils.text import slugify, phone2numeric

from programs.models import Program, ProgramInitRequirements, PhdStudent, Student, StudentInitRequirement, ProgramMember
from programs.utils import user_is_program_cs


def index(request, program_slug):
    if not request.user.is_authenticated :
        context={
            'program': Program.objects.get(slug=program_slug)
        }
        return render(request,'programs/program_index.html', context)
    else:
        return HttpResponseRedirect(reverse('programs:home', args=[program_slug]))


@login_required
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


@login_required
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


@login_required
def students_list(request, program_slug, scope):
    program=Program.objects.get(slug=program_slug)
    if scope == 'all':
        context={
            'program': program,
            'students': Student.objects.filter(program=program),
        }
    elif scope == 'requesters':
        context={
            'program': program,
            'students': Student.objects.filter(program=program, phdstudent__status='solicitante'),
        }
    elif scope == 'aproved':
        context = {
            'program': program,
            'students': Student.objects.filter(program=program, phdstudent__status = 'doctorando'),
        }
    elif scope == 'graduated':
        context = {
            'program': program,
            'students': Student.objects.filter(program=program, phdstudent__status = 'graduado'),
        }

    return render(request, 'programs/students_list.html', context)

@login_required
def edit_student(request, program_slug, student_id):
    program= Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method == 'POST':
            user=Student.objects.get(pk=student_id).user
            user.first_name=request.POST['student_name']
            user.last_name=request.POST['student_surename']
            user.email=request.POST['student_email']
            user.save()

            Student.objects.filter(pk=student_id).update(
                phone=request.POST['student_phone'],
                country=request.POST['student_country']
                            )
            try:
                if request.FILES['student_picture']:
                    Student.objects.filter(pk=student_id).update(
                        picture=request.FILES['student_picture']
                    )
            except:
                pass

            for requirement in ProgramInitRequirements.objects.filter(program=program):
                if 'student_requirement_' + str(requirement.id) in request.POST:
                    s_i_r=StudentInitRequirement.objects.get(student=Student.objects.get(pk=student_id), requirement=requirement)
                    s_i_r.accomplished=True
                    s_i_r.save()
                else:
                    s_i_r = StudentInitRequirement.objects.get(student=Student.objects.get(pk=student_id),
                                                               requirement=requirement)
                    s_i_r.accomplished = False
                    s_i_r.save()

            return HttpResponseRedirect(reverse('programs:students_list', args=[program_slug,'all']))
        else:
            context = {
                'program': program,
                'student': Student.objects.get(pk=student_id),
                'init_requirements': ProgramInitRequirements.objects.filter(program=program)
            }
            return render(request, 'programs/edit_phd_student.html', context)
    else:
        return HttpResponse('Error: Usuario no CS')


