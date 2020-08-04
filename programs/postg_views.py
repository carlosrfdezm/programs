import json
import os
import random
import calendar, locale
import zipfile

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail, send_mass_mail
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from django.urls import reverse
from django.utils import dateparse
from django.utils.text import slugify, phone2numeric
from django.utils.timezone import now

from programas.settings import MEDIA_URL, MEDIA_ROOT
from programs.models import Program, ProgramInitRequirements, PhdStudent, Student, StudentInitRequirement, \
    ProgramMember, ProgramFinishRequirements, StudentFinishRequirement, InvestigationLine, PhdStudentTheme, \
    InvestigationProject, ProgramBackgrounds, MscStudent, ProgramEdition, MscStudentTheme, DipStudent, CGC_Member, \
    CGCBrief, CNGCBrief, PostgMember
from programs.templatetags.extra_tags import init_requirements_accomplished, finish_requirements_accomplished
from programs.utils import user_is_program_cs, user_is_program_member, utils_send_email, user_is_program_student, \
    user_is_cgc_member, user_is_cgc_ps

from docx import Document
from docx.shared import Inches
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

def index(request):
    context={
        'members':PostgMember.objects.all(),
        'director':PostgMember.objects.get(charge='Director'),
        'programs': Program.objects.all().order_by('-type'),
    }
    return render(request, 'programs/postg/postg_index.html', context)

@login_required
def home(request):
    try:
        postg_member=PostgMember.objects.get(user=request.user)
        context={
            'member':postg_member,
            'phd_programs': Program.objects.filter(type='phd').__len__(),
            'msc_programs': Program.objects.filter(type='msc').__len__(),
            'dip_programs': Program.objects.filter(type='dip').__len__(),
            'postg_members': PostgMember.objects.all().__len__(),
        }
        return render(request, 'programs/postg/postg_home.html', context)

    except PostgMember.DoesNotExist:
        return error_500(request,"Usted no es miembro de la Direccion de Postgrado")




def error_500(request, error_message):
    context={

        'error_message':error_message,
    }
    try:
        context['member'] = PostgMember.objects.get(user=request.user)
    except Exception:
        pass

    return render(request,'programs/postg/postg_error_500.html', context)

def logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('postg:postg_home'))

@login_required
def ajx_postg_phd_students_by_program(request):
    response_data=[]
    labels = []
    data = []
    for program in Program.objects.filter(type='phd'):
        labels.append(program.slug.upper())
        data.append(program.student_set.all().__len__())

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    response_data.append(labels)
    response_data.append(data)




    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_postg_msc_students_by_program(request):
    response_data=[]
    labels = []
    data = []
    for program in Program.objects.filter(type='msc'):
        labels.append(program.slug.upper())
        data.append(program.mscstudent_set.filter(status='maestrante').__len__())

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    response_data.append(labels)
    response_data.append(data)




    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def ajx_postg_dip_students_by_program(request):
    response_data=[]
    labels = []
    data = []
    for program in Program.objects.filter(type='dip'):
        labels.append(program.slug.upper())
        data.append(program.dipstudent_set.filter(status='diplomante').__len__())

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    response_data.append(labels)
    response_data.append(data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def programs(request, program_type):
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context={
            'member': postg_member,
            'programs': Program.objects.filter(type=program_type),
            'program_type': program_type,

        }
        return render(request, "programs/postg/postg_programs_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')


@login_required
def members(request):
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context={
            'member': postg_member,
            'members': PostgMember.objects.all(),

        }
        return render(request, "programs/postg/postg_members_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')



@login_required
def lines(request):
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context={
            'member': postg_member,
            'programs': Program.objects.all(),

        }
        return render(request, "programs/postg/postg_lines_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')

@login_required
def lines(request):
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context={
            'member': postg_member,
            'programs': Program.objects.all(),

        }
        return render(request, "programs/postg/postg_lines_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')


@login_required
def program_students(request, program_slug, scope):
    program = Program.objects.get(slug = program_slug)
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context = {
            'member': postg_member,
            'program': program,
            'scope':scope,
        }
        if program.type == 'phd':
            if scope == 'all':
                context['students'] = PhdStudent.objects.filter(student__program=program)
            elif scope == 'requesters':
                context['students'] = PhdStudent.objects.filter(student__program=program, status='solicitante')
            elif scope == 'approved':
                context['students'] = PhdStudent.objects.filter(student__program=program, status='doctorando')
            elif scope == 'graduated':
                context['students'] = PhdStudent.objects.filter(student__program=program, status='graduado')
            else:
                return error_500(request,
                                 'El contexto "' + scope + '" no se admite. Debe ser "all", "approved", "requesters" o "graduated" ')
                
        elif program.type == 'msc':
            if scope == 'all':
                context['students'] = MscStudent.objects.filter(program=program)
            elif scope == 'requesters':
                context['students'] = MscStudent.objects.filter(program=program, status='solicitante')
            elif scope == 'approved':
                context['students'] = MscStudent.objects.filter(program=program, status='maestrante')
            elif scope == 'graduated':
                context['students'] = MscStudent.objects.filter(program=program, status='graduado')
            else:
                return error_500(request,
                                 'El contexto "' + scope + '" no se admite. Debe ser "all", "approved", "requesters" o "graduated" ')
            
        elif program.type == 'dip':
            if scope == 'all':
                context['students'] = DipStudent.objects.filter(program=program)
            elif scope == 'requesters':
                context['students'] = DipStudent.objects.filter(program=program, status='solicitante')
            elif scope == 'approved':
                context['students'] = DipStudent.objects.filter(program=program, status='diplomante')
            elif scope == 'graduated':
                context['students'] = DipStudent.objects.filter(program=program, status='graduado')
            else:
                return error_500(request, 'El contexto "'+ scope +'" no se admite. Debe ser "all", "approved", "requesters" o "graduated" ')




        return render(request, "programs/postg/postg_students_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')


@login_required
def program_members(request, program_slug, scope):
    program = Program.objects.get(slug=program_slug)
    try:
        postg_member = PostgMember.objects.get(user=request.user)

        context = {
            'member': postg_member,
            'program': program,
            'scope': scope,
        }

        if scope == 'all':
            context['program_members'] = ProgramMember.objects.filter(program=program)
        elif scope == 'committee':
            context['program_members'] = ProgramMember.objects.filter(Q(role='Coordinador')| Q(role='Secretario')| Q(role='Miembro'),program=program)
        elif scope == 'proffessor':
            context['program_members'] = ProgramMember.objects.filter(program=program, role='Profesor')
        elif scope == 'tuthor':
            context['program_members'] = ProgramMember.objects.filter(program=program, role='Tutor')
        else:
            return error_500(request,
                             'El contexto "' + scope + '" no se admite. Por favor acceda desde algún enlace válido del sitio ')

        return render(request, "programs/postg/postg_program_members_list.html", context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no es miembro de la Dirección de Postgrado')

@login_required
def program_statistics(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    try:
        postg_member = PostgMember.objects.get(user=request.user)
        context={
            'member':postg_member,
            'program':program,
        }

        return render(request, 'programs/postg/postg_program_statistics.html', context)
    except PostgMember.DoesNotExist:
        return error_500(request, 'Usted no tiene privilegios para acceder a esta página')


@login_required
def ajx_members_by_grade(request, program_slug):
    response_data=[]
    grades=[]
    data=[]

    program = Program.objects.get(slug=program_slug)
    for member in ProgramMember.objects.filter(program=program):
        if not member.degree in grades:
            grades.append(member.degree)

    for degree in grades:
        data.append(ProgramMember.objects.filter(program=program, degree=degree).__len__())

    response_data.append(grades)
    response_data.append(data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_students_by_line(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data=[]
    labels = []
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    for line in InvestigationLine.objects.filter(program=Program.objects.get(slug=program_slug)):
        i += 1
        labels.append(line.name.split()[0])
        if program.type == 'phd':
            data.append(PhdStudentTheme.objects.filter(line=line).__len__())
        elif program.type == 'msc':
            data.append(MscStudentTheme.objects.filter(line=line).__len__())


    response_data.append(labels)
    response_data.append(data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def ajx_students_by_edition(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data=[]
    labels = []
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for edition in ProgramEdition.objects.filter(program=program):
        labels.append('Edición '+str(edition.order))
        if program.type == 'msc':
            data.append(MscStudent.objects.filter(Q(status='maestrante')|Q(status='graduado'), program=program, edition=edition).__len__())
        elif program.type == 'dip':
            data.append(DipStudent.objects.filter(Q(status='diplomante')|Q(status='graduado'), program=program, edition=edition).__len__())



    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def ajx_graduated_by_edition(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data = []
    labels = []
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for edition in ProgramEdition.objects.filter(program=program):
        labels.append('Edición ' + str(edition.order))
        if program.type == 'msc':
            data.append(
                MscStudent.objects.filter(program=program, edition=edition, status='graduado').__len__())
        elif program.type == 'dip':
            data.append(
                DipStudent.objects.filter(program=program, edition=edition, status='graduado').__len__())

    response_data.append(labels)
    response_data.append(data)

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_students_by_gender(request, program_slug):

    response_data=[]
    program=Program.objects.get(slug=program_slug)
    if program.type == 'phd':
        response_data.append(Student.objects.filter(program=program, gender='f').__len__())
        response_data.append(Student.objects.filter(program=program, gender='m').__len__())
    elif program.type == 'msc':
        response_data.append(MscStudent.objects.filter(program=program, gender='f').__len__())
        response_data.append(MscStudent.objects.filter(program=program,gender='m').__len__())
    elif program.type == 'dip':
        response_data.append(DipStudent.objects.filter(program=program, gender='f').__len__())
        response_data.append(DipStudent.objects.filter(program=program, gender='m').__len__())

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_students_by_age(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data=[]
    labels = ['<30 años','30-40','40-50','>50 años']
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    if program.type == 'phd':
        data.append(Student.objects.filter(program=program,birth_date__year__gte=now().year-30 ).__len__())
        data.append(Student.objects.filter(program=program,birth_date__year__gte=now().year-40, birth_date__year__lt=now().year-30 ).__len__() )
        data.append(Student.objects.filter(program=program,birth_date__year__gte=now().year-50, birth_date__year__lt=now().year-40 ).__len__() )
        data.append(Student.objects.filter(program=program, birth_date__year__lte=now().year-50 ).__len__() )
    elif program.type == 'msc':
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gte=now().year - 30).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gte=now().year - 40,
                                              birth_date__year__lt=now().year - 30).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gte=now().year - 50,
                                              birth_date__year__lt=now().year - 40).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__lte=now().year - 50).__len__())
    elif program.type == 'dip':
        data.append(DipStudent.objects.filter(program=program, birth_date__year__gte=now().year - 30).__len__())
        data.append(DipStudent.objects.filter(program=program, birth_date__year__gte=now().year - 40,
                                              birth_date__year__lt=now().year - 30).__len__())
        data.append(DipStudent.objects.filter(program=program, birth_date__year__gte=now().year - 50,
                                              birth_date__year__lt=now().year - 40).__len__())
        data.append(DipStudent.objects.filter(program=program, birth_date__year__lte=now().year - 50).__len__())


    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def postg_by_line_projects_list(request, line_id):
    line = InvestigationLine.objects.get(pk=line_id)
    try:
        postg_member = PostgMember.objects.get(user=request.user)
        context={
            'member':postg_member,
            'line': line,
            'projects': InvestigationProject.objects.filter(line=line),
        }
        return render(request, 'programs/postg/postg_by_line_projects_list.html', context)


    except PostgMember.DoesNotExist:
        return error_500(request,  'Usted no tiene privilegios para acceder a esta página')

