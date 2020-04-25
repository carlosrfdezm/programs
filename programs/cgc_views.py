import json
import random
import calendar, locale


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

from programs.models import Program, ProgramInitRequirements, PhdStudent, Student, StudentInitRequirement, \
    ProgramMember, ProgramFinishRequirements, StudentFinishRequirement, InvestigationLine, PhdStudentTheme, \
    InvestigationProject, ProgramBackgrounds, MscStudent, ProgramEdition, MscStudentTheme, DipStudent, CGC_Member, \
    CGCBrief
from programs.utils import user_is_program_cs, user_is_program_member, utils_send_email, user_is_program_student, \
    user_is_cgc_member, user_is_cgc_ps


@login_required
def cgc_home(request):
    context = {
        'cgc_member': CGC_Member.objects.get(user=request.user),
        'phd_programs': Program.objects.filter(type='phd'),
        'requesters': PhdStudent.objects.filter(status='solicitante').__len__(),
        'doctorands': PhdStudent.objects.filter(status='doctorando').__len__(),
        'graduated': PhdStudent.objects.filter(status='graduado').__len__(),
        'members': CGC_Member.objects.all().__len__(),
    }
    return render(request, 'programs/cgc/cgc_home.html', context)

@login_required
def create_cgc_brief(request):
    if user_is_cgc_ps(request.user):
        if request.method == 'POST':
            # try:
            brief = request.FILES['brief']

            new_brief = CGCBrief(
                brief=brief,
                year=request.POST['year'],
                month=request.POST['month'],
            )
            new_brief.save()
            return HttpResponseRedirect(reverse('cgc:cgc_year_brieffings', args=[new_brief.year]))

        # except:
        #     print('Excepcion lanzada')
        #     return error_500(request, 'Ha ocurrido un error al crear la nueva acta')


        else:
            meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
                     8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
            context = {
                'months': ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio','Agosto', 'Septiembre',
                           'Octubre', 'Noviembre', 'Diciembre'],
                'current_month': meses[now().month],
                'years':range(now().year-10,now().year+1),
                'current_year':now().year,
            }
            return render(request, 'programs/cgc/cgc_create_brief.html',context)
    else:
        return error_500(request,'Usted no tiene privilegios para agregar actas.')

@login_required
def cgc_year_brieffings(request, year):
    years = []
    for brieffing in CGCBrief.objects.all():
        if not brieffing.year in years:
            years.append(brieffing.year)
    if user_is_cgc_member(request.user):
        context={
            'year':year,
            'years':years,
            'brieffings': CGCBrief.objects.filter(year=year),
        }
        return render(request, 'programs/cgc/cgc_brieffings_list.html',context)
    else:
        return error_500(request,'Usted no puede ver las actas de la CGC')

@login_required
def cgc_brieffings(request):
    if user_is_cgc_member(request.user):
        years=[]
        for brieffing in CGCBrief.objects.all():
            if not brieffing.year in years:
                years.append(brieffing.year)

        context={
            'years': sorted(years),
            'brieffings': CGCBrief.objects.all(),
        }
        return render(request, 'programs/cgc/cgc_brieffings_list.html',context)
    else:
        return error_500(request,'Usted no puede ver las actas de la CGC')

def cgc_brief_view(request, brief_id):

    brieffing = CGCBrief.objects.get(pk=brief_id)

    fs = FileSystemStorage()

    filename =brieffing.brief.url

    if fs.exists(filename):
        brief_ext =filename.split('.')[filename.split('.').__len__()-1]

        if brief_ext =='doc' or brief_ext=='docx' or brief_ext == 'docx':

            with fs.open(filename) as brief:
                response = HttpResponse(brief, content_type='application/doc')
                response['Content-Disposition'] =  "inline; filename=" + '"'+'Acta_CGC_'+ brieffing.month+'_'+str(brieffing.year)+'.'+brief_ext+'"'

                return response

        elif brief_ext == 'pdf' :
            with fs.open(filename) as brief:
                response = HttpResponse(brief, content_type='application/pdf')
                response['Content-Disposition'] = "inline; filename=" + '"'+'Acta_CGC_' + brieffing.month+'_'+str(brieffing.year)+'.'+brief_ext + '"'

                return response

    else:


        return error_500(request, 'No existe el archivo solicitado')

@login_required
def students_list(request, scope):
    if user_is_cgc_member(request.user):

        if scope == 'all':
            context = {
                'students': Student.objects.all(),
                'scope': 'all',
            }
        elif scope == 'requesters':
            context = {
                'students': Student.objects.filter( phdstudent__status='solicitante'),
                'scope': 'Solicitantes',
            }
        elif scope == 'aproved':
            context = {
                'students': Student.objects.filter( phdstudent__status='doctorando'),
                'scope': 'Doctorandos',
            }
        elif scope == 'graduated':
            context = {
                'students': Student.objects.filter( phdstudent__status='graduado'),
                'scope': 'Graduados',
            }

        return render(request, 'programs/cgc/cgc_students_list.html', context)


    else:
        return error_500(request, 'Usted no tiene acceso a esta página')

@login_required
def program_members_list(request,program_slug):
    program = Program.objects.get(slug=program_slug)

    if user_is_cgc_member(request.user):


        context = {
            'phd_program' : program,
            'members': ProgramMember.objects.filter(program=program),
            'scope': 'all',
        }


        return render(request, 'programs/cgc/cgc_program_members_list.html', context)


    else:
        return error_500(request, 'Usted no tiene acceso a esta página')


@login_required
def program_students_list(request, program_slug, scope):
    program = Program.objects.get(slug=program_slug)

    if user_is_cgc_member(request.user):

        if scope == 'all':
            context = {
                'phd_program': program,
                'students': Student.objects.filter(program=program),
                'scope': 'all',
            }
        elif scope == 'requesters':
            context = {
                'phd_program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='solicitante'),
                'scope': 'Solicitantes',
            }
        elif scope == 'aproved':
            context = {
                'phd_program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='doctorando'),
                'scope': 'Doctorandos',
            }
        elif scope == 'graduated':
            context = {
                'phd_program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='graduado'),
                'scope': 'Graduados',
            }

        return render(request, 'programs/cgc/cgc_students_list.html', context)


    else:
        return error_500(request, 'Usted no tiene acceso a esta página')



@login_required
def programs_lines(request):

    if user_is_cgc_member(request.user):

        context={
            'programs': Program.objects.filter(type='phd')
        }
        return render(request, 'programs/cgc/cgc_lines_list.html', context)

    else:
        return error_500(request, 'Usted no tiene acceso a esta página')

@login_required
def programs_projects(request):

    if user_is_cgc_member(request.user):

        context={
            'programs': Program.objects.filter(type='phd')
        }
        return render(request, 'programs/cgc/cgc_projects_list.html', context)

    else:
        return error_500(request, 'Usted no tiene acceso a esta página')


def error_500(request, error_message):
    context={

        'error_message':error_message,
    }
    return render(request,'programs/cgc/cgc_error_500.html', context)




@login_required
def program_lines(request, program_slug):
    context={
        'program': Program.objects.get(slug=program_slug),
        'lines': InvestigationLine.objects.filter(program=Program.objects.get(slug=program_slug)),
    }
    return render(request, 'programs/lines_list.html', context)

@login_required
def students_by_line(request, program_slug, line_id):
    program=Program.objects.get(slug=program_slug)
    line=InvestigationLine.objects.get(pk=line_id)
    context={
        'program':program,
        'line':line,
        'students':Student.objects.filter(phdstudent__phdstudenttheme__line=line)
    }
    return render(request, 'programs/students_by_line.html', context)


@login_required
def projects_list(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    context={
        'program':program,
        'projects':InvestigationProject.objects.filter(program=program)
    }
    return render(request, 'programs/projects_list.html',context)



@login_required
def ajx_delete_member(request, program_slug):
    program=Program.objects.get(slug=program_slug)

    if user_is_program_cs(request.user,program ):
        if request.method=='POST':
            member_id=request.POST['member_id']
            try:
                ProgramMember.objects.get(pk=member_id).delete()
                return HttpResponse(
                    json.dumps([{'deleted': 1}]),
                    content_type="application/json"
                )
            except:
                return HttpResponse(
                    json.dumps([{'deleted': 0}]),
                    content_type="application/json"
                )
        else:
            return HttpResponse(
                json.dumps([{'deleted': 0}]),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps([{'deleted': 0}]),
            content_type="application/json"
        )


@login_required
def ajx_delete_cgc_brieffing(request):

    if user_is_cgc_ps(request.user ):
        if request.method=='POST':
            brief_id=request.POST['brief_id']
            try:
                CGCBrief.objects.get(pk=brief_id).delete()
                return HttpResponse(
                    json.dumps([{'deleted': 1}]),
                    content_type="application/json"
                )
            except:
                return HttpResponse(
                    json.dumps([{'deleted': 0}]),
                    content_type="application/json"
                )
        else:
            return HttpResponse(
                json.dumps([{'deleted': 0}]),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps([{'deleted': 2}]),
            content_type="application/json"
        )


@login_required
def ajx_last_years_requests(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data=[]
    labels = []
    data = []
    data_1=[]
    data_2=[]

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for i in range(now().year-4,now().year+1):
        labels.append(i)
        if program.type == 'phd':
            data_1.append(Student.objects.filter(request_date__year=i).__len__())
            data_2.append(Student.objects.filter(init_date__year=i).__len__())
        elif program.type == 'msc':
            data_1.append(MscStudent.objects.filter(request_date__year=i).__len__())
            data_2.append(MscStudent.objects.filter(init_date__year=i).__len__())
        elif program.type == 'dip':
            data_1.append(DipStudent.objects.filter(request_date__year=i).__len__())
            data_2.append(DipStudent.objects.filter(init_date__year=i).__len__())

    data.append(data_1)
    data.append(data_2)

    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )


@login_required
def ajx_last_years_requests_vs_graduated(request):
    response_data=[]
    labels = []
    data = []
    data_1=[]
    data_2=[]

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for i in range(now().year-4,now().year+1):
        labels.append(i)
        data_1.append(Student.objects.filter(init_date__year=i).__len__())
        data_2.append(Student.objects.filter(graduate_date__year=i).__len__())




    data.append(data_1)
    data.append(data_2)

    response_data.append(labels)
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
def ajx_students_by_age(request, program_slug):
    program = Program.objects.get(slug=program_slug)
    response_data=[]
    labels = ['<30 años','30-40','40-50','>50 años']
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    if program.type == 'phd':
        data.append(Student.objects.filter(program=program,birth_date__year__gt=now().year-30 ).__len__())
        data.append(Student.objects.filter(program=program,birth_date__year__gt=now().year-40, birth_date__year__lt=now().year-30 ).__len__() )
        data.append(Student.objects.filter(program=program,birth_date__year__gt=now().year-50, birth_date__year__lt=now().year-40 ).__len__() )
        data.append(Student.objects.filter(program=program, birth_date__year__lt=now().year-50 ).__len__() )
    elif program.type == 'msc':
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gt=now().year - 30).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gt=now().year - 40,
                                              birth_date__year__lt=now().year - 30).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__gt=now().year - 50,
                                              birth_date__year__lt=now().year - 40).__len__())
        data.append(MscStudent.objects.filter(program=program, birth_date__year__lt=now().year - 50).__len__())
    elif program.type == 'dip':
        pass


    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def programs_members_list(request, scope):
    if user_is_cgc_member(request.user):
        users=[]
        if scope == 'all':
            for member in ProgramMember.objects.filter(program__type='phd'):
                if not member.user in users:
                    users.append(member.user)
                else:
                    pass

            context={
                'users': users,
                'scope':scope,
            }
        elif scope == 'comite':
            for member in ProgramMember.objects.filter(Q(role='Coordinador')|Q(role='Secretario')|Q(role='Miembro'), program__type='phd'):
                if not member.user in users:
                    users.append(member.user)
                else:
                    pass
            context = {
                'users': users,
                'scope': 'Comité Doctorales',
            }

        return render(request, 'programs/cgc/cgc_programs_members_list.html', context)

@login_required
def cgc_programs_list(request):
    if user_is_cgc_member(request.user):
        context={
            'programs': Program.objects.filter(type='phd').order_by('full_name'),

        }

        return render(request, 'programs/cgc/cgc_programs_list.html', context)
    else:
        return error_500(request, 'Usted no tiene acceso a esta vista.')

@login_required
def ajx_member_personal_msg(request, program_slug ):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST' and request.POST['msg_body'].__len__() <= 500:
        try:
            send_mail(request.POST['msg_subject'], request.POST['msg_body'],request.user.email,
                      [ProgramMember.objects.get(pk=request.POST['member_id']).user.email],
                      fail_silently=False,html_message=request.POST['msg_body'])
            return HttpResponse(
                json.dumps([{'sended': 1}]),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps([{'sended': 0}]),
                content_type="application/json"
            )
    elif request.method == 'POST' and request.POST['msg_body'].__len__() > 500:
        return HttpResponse(
            json.dumps([{'sended': 2}]),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps([{'sended': 0}]),
            content_type="application/json"
        )

@login_required
def ajx_member_massive_msg(request, program_slug ):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST' and request.POST['msg_body'].__len__() <= 500:
        try:
            email_list = []
            if request.POST['msg_scope'] == 'comite':
                for member in ProgramMember.objects.filter(Q(role='Coordinador')|Q(role='Secretario')|Q(role='Miembro'), program=program  ):
                    email_list.append(member.user.email)
            elif request.POST['msg_scope']=='professors':
                for member in ProgramMember.objects.filter(program=program , role='Profesor' ):
                    email_list.append(member.user.email)
            elif request.POST['msg_scope']=='tuthors':
                for member in ProgramMember.objects.filter(program=program , role='Tutor' ):
                    email_list.append(member.user.email)

            elif request.POST['msg_scope']=='all':
                for member in ProgramMember.objects.filter(program=program ):
                    email_list.append(member.user.email)

            if email_list.__len__()<=10:
                send_mail(request.POST['msg_subject'], request.POST['msg_body'],request.user.email,
                          email_list, fail_silently=False, html_message=request.POST['msg_body'])
            else:
                count = email_list.__len__() // 10
                rest = email_list.__len__() % 10

                for i in range(count):
                    print(i)
                    send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                              request.user.email,
                              email_list[10 * i:10 * (i + 1)], fail_silently=False, html_message=request.POST['msg_body'])

                    if rest != 0:
                        send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                                  request.user.email,
                                  email_list[10 * count:10 * count + rest], fail_silently=False,
                                  html_message=request.POST['msg_body'])



            return HttpResponse(
                json.dumps([{'sended': 1}]),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps([{'sended': 0}]),
                content_type="application/json"
            )
    elif request.method == 'POST' and request.POST['msg_body'].__len__() > 500:
        return HttpResponse(
            json.dumps([{'sended': 2}]),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps([{'sended': 0}]),
            content_type="application/json"
        )

@login_required
def ajx_everybody_massive_msg(request, program_slug ):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST' and request.POST['msg_body'].__len__() <= 500:
        try:
            email_list = []
            for member in ProgramMember.objects.filter(program=program):
                email_list.append(member.user.email)
            for student in Student.objects.filter(program=program):
                email_list.append(student.user.email)

            if email_list.__len__()<=10:
                send_mail(request.POST['msg_subject'], request.POST['msg_body'],request.user.get_full_name + request.user.email,
                          email_list, fail_silently=False, html_message=request.POST['msg_body'])
            else:
                count = email_list.__len__() // 10
                rest = email_list.__len__() % 10

                for i in range(count):
                    print(i)
                    send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                              request.user.get_full_name + request.user.email,
                              email_list[10 * i:10 * (i + 1)], fail_silently=False, html_message=request.POST['msg_body'])

                    if rest != 0:
                        send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                                  request.user.get_full_name + request.user.email,
                                  email_list[10 * count:10 * count + rest], fail_silently=False,
                                  html_message=request.POST['msg_body'])



            return HttpResponse(
                json.dumps([{'sended': 1}]),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps([{'sended': 0}]),
                content_type="application/json"
            )
    elif request.method == 'POST' and request.POST['msg_body'].__len__() > 500:
        return HttpResponse(
            json.dumps([{'sended': 2}]),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps([{'sended': 0}]),
            content_type="application/json"
        )

@login_required
def ajx_students_massive_msg(request, program_slug ):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST' and request.POST['msg_body'].__len__() <= 500:
        try:
            email_list = ['boris_perez@unah.edu.cu']
            if program.type == 'phd':
                if request.POST['msg_scope'] == 'requesters':
                    for student in PhdStudent.objects.filter(program=program ,status='solicitante' ):
                        email_list.append(student.user.email)
                elif request.POST['msg_scope']=='aproved':
                    for student in PhdStudent.objects.filter(program=program ,status='doctorando' ):
                        email_list.append(student.user.email)

                elif request.POST['msg_scope']=='graduated':
                    for student in PhdStudent.objects.filter(program=program, status='graduado'):
                        email_list.append(student.user.email)

                elif request.POST['msg_scope']=='all':
                    for student in PhdStudent.objects.filter(program=program):
                        email_list.append(student.user.email)
            elif program.type == 'msc':
                if request.POST['msg_scope'] == 'requesters':
                    for student in MscStudent.objects.filter(program=program, status='solicitante'):
                        email_list.append(student.user.email)
                elif request.POST['msg_scope'] == 'aproved':
                    for student in MscStudent.objects.filter(program=program, status='maestrante'):
                        email_list.append(student.user.email)

                elif request.POST['msg_scope'] == 'graduated':
                    for student in MscStudent.objects.filter(program=program, status='graduado'):
                        email_list.append(student.user.email)

                elif request.POST['msg_scope'] == 'all':
                    for student in MscStudent.objects.filter(program=program):
                        email_list.append(student.user.email)
            elif program.type == 'dip':
                pass

            if email_list.__len__()<=10:
                send_mail(request.POST['msg_subject'], request.POST['msg_body'],request.user.email,
                          email_list, fail_silently=False, html_message=request.POST['msg_body'])
            else:
                count = email_list.__len__() // 10
                rest = email_list.__len__() % 10

                for i in range(count):
                    print(i)
                    send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                              request.user.email,
                              email_list[10 * i:10 * (i + 1)], fail_silently=False, html_message=request.POST['msg_body'])

                    if rest != 0:
                        send_mail(request.POST['msg_subject'], request.POST['msg_body'],
                                  request.user.email,
                                  email_list[10 * count:10 * count + rest], fail_silently=False,
                                  html_message=request.POST['msg_body'])



            return HttpResponse(
                json.dumps([{'sended': 1}]),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps([{'sended': 0}]),
                content_type="application/json"
            )
    elif request.method == 'POST' and request.POST['msg_body'].__len__() > 500:
        return HttpResponse(
            json.dumps([{'sended': 2}]),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps([{'sended': 0}]),
            content_type="application/json"
        )

@login_required
def ajx_student_personal_msg(request, program_slug ):
    program=Program.objects.get(slug=program_slug)
    if request.method == 'POST' and request.POST['msg_body'].__len__() <= 500:
        try:
            if program.type == 'phd':
                send_mail(request.POST['msg_subject'], request.POST['msg_body'],request.user.email,
                          [Student.objects.get(pk=request.POST['student_id']).user.email,'boris_perez@unah.edu.cu'],
                          fail_silently=False,html_message=request.POST['msg_body'])
            elif program.type == 'msc':
                send_mail(request.POST['msg_subject'], request.POST['msg_body'], request.user.email,
                          [MscStudent.objects.get(pk=request.POST['student_id']).user.email, 'boris_perez@unah.edu.cu'],
                          fail_silently=False, html_message=request.POST['msg_body'])
            elif program.type == 'dip':
                pass

            return HttpResponse(
                json.dumps([{'sended': 1}]),
                content_type="application/json"
            )
        except:
            return HttpResponse(
                json.dumps([{'sended': 0}]),
                content_type="application/json"
            )
    elif request.method == 'POST' and request.POST['msg_body'].__len__() > 500:
        return HttpResponse(
            json.dumps([{'sended': 2}]),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps([{'sended': 0}]),
            content_type="application/json"
        )

@login_required
def ajx_members_by_age(request, program_slug):
    response_data=[]
    labels = ['<30 años','30-40','40-50','>50 años']
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    data.append(ProgramMember.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-30 ).__len__())
    data.append(ProgramMember.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-40, birth_date__year__lt=now().year-30 ).__len__() )
    data.append(ProgramMember.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-50, birth_date__year__lt=now().year-40 ).__len__() )
    data.append(ProgramMember.objects.filter(program=Program.objects.get(slug=program_slug ), birth_date__year__lt=now().year-50 ).__len__() )


    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )



@login_required
def ajx_students_by_state(request):
    response_data=[]
    data = []


    labels = ['Graduados', 'Solicitantes', 'Doctorandos']
    data.append(PhdStudent.objects.filter( status='graduado').__len__())
    data.append(PhdStudent.objects.filter( status='solicitante').__len__())
    data.append(PhdStudent.objects.filter( status='doctorando').__len__())

    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

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
def ajx_students_by_sex(request, program_slug):

    response_data=[]
    program=Program.objects.get(slug=program_slug)
    if program.type == 'phd':
        response_data.append(PhdStudent.objects.filter(student__program=program, student__gender='f').__len__())
        response_data.append(PhdStudent.objects.filter(student__program=program, student__gender='m').__len__())
    elif program.type == 'msc':
        response_data.append(MscStudent.objects.filter(program=program, gender='f').__len__())
        response_data.append(MscStudent.objects.filter(program=program,gender='m').__len__())
    elif program.type == 'dip':
        pass

    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def program_statistics(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        context={
            'program':program,
        }
        return render(request, 'programs/statistics.html', context)


@login_required
def ajx_cgc_this_year_requests(request):
    response_data=[]
    labels = []
    data = []
    data_1=[]
    data_2=[]
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
             8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for i in range(1,now().month+1):
        labels.append(meses[i])

        data_1.append(Student.objects.filter(request_date__year=now().year,request_date__month=i).__len__())
        data_2.append(Student.objects.filter(init_date__year=now().year,init_date__month=i).__len__())


    data.append(data_1)
    data.append(data_2)

    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

