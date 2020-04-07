import json
import random
import calendar, locale


from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
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
    InvestigationProject, ProgramBackgrounds
from programs.utils import user_is_program_cs, user_is_program_member, utils_send_email


def index(request, program_slug):
    if not request.user.is_authenticated :
        program = Program.objects.get(slug=program_slug)

        context = {
            'program': program,

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
            'last_requesters': PhdStudent.objects.filter(student__program=program, status='solicitante').order_by('-student__request_date')[:4],
            'last_aproved': PhdStudent.objects.filter(student__program=program, status='doctorando').order_by('-student__request_date')[:4],
            'last_graduated': PhdStudent.objects.filter(student__program=program, status='graduado').order_by('-student__request_date')[:4],

        }
        return render(request, 'programs/phd_home.html', context)
    else:
        pass


@login_required
def create_student(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method == 'POST':
            try:
                user = User.objects.get(email=request.POST['student_email'])
            except User.DoesNotExist:
                passwd = program_slug + str(random.randint(1000000, 9999999))
                user = User.objects.create_user(
                    request.POST['student_email'],
                    request.POST['student_email'],
                    passwd,  # Cambiar despues por contrase;a generada

                )
                user.first_name = request.POST['student_name']
                user.last_name = request.POST['student_surename']
                user.save()

            student = Student(
                user=user,
                program=program,
                gender=request.POST['gender'],
                dni=request.POST['student_dni'],
                birth_date=request.POST['student_birth_date'],
            )
            student.save()

            utils_send_email(request, 'wm', program.email, student, '', '', program, passwd)

            try:
                student.picture=request.FILES['picture']
                student.save()



            except:
                pass

            if program.type=='phd':
                new_student = PhdStudent(
                    student=student,
                    status='solicitante',
                )
                new_student.save()
                new_theme=PhdStudentTheme(
                    phd_student=new_student,
                    description=request.POST['theme'],
                )
                try:
                    new_theme.project=InvestigationProject.objects.get(pk=request.POST['investigation_project'])
                    new_theme.line=InvestigationProject.objects.get(pk=request.POST['investigation_project']).line,

                except:
                    pass

                new_theme.save()
            else:
                return HttpResponse('Tipo de programa aun por crear')

            for requirement in ProgramInitRequirements.objects.filter(program=program):

                if 'student_requirement_' + str(requirement.id) in request.POST:
                    new_student_requirement = StudentInitRequirement(
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

            return HttpResponseRedirect(reverse('programs:students_list', args=[program_slug, 'all']))
        else:
            context = {
                'program': program,
                'init_requirements': ProgramInitRequirements.objects.filter(program=program),
                'projects': InvestigationProject.objects.filter(program=program),
            }
            if Program.objects.get(slug=program_slug).type == 'phd':
                return render(request, 'programs/create_phd_student.html', context)
            else:
                return HttpResponse('El programa no es un doctorado')
    else:
        return HttpResponse('Error, acceso solo a coordinadores y secretarios')


@login_required
def students_list(request, program_slug, scope):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_member(request.user, program):
        if scope == 'all':
            context = {
                'program': program,
                'students': Student.objects.filter(program=program),
                'scope':'all',
            }
        elif scope == 'requesters':
            context = {
                'program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='solicitante'),
                'scope': 'Solicitantes',
            }
        elif scope == 'aproved':
            context = {
                'program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='doctorando'),
                'scope': 'Doctorandos',
            }
        elif scope == 'graduated':
            context = {
                'program': program,
                'students': Student.objects.filter(program=program, phdstudent__status='graduado'),
                'scope': 'Graduados',
            }

        return render(request, 'programs/students_list.html', context)
    else:
        return error_500(request, program, 'Usted no tiene acceso a esta página')

@login_required
def members_list(request, program_slug, scope):
    program=Program.objects.get(slug=program_slug)
    if scope == 'all':
        context = {
            'program': program,
            'members': ProgramMember.objects.filter(program=program),
            'scope': 'all',
        }
    elif scope == 'comite':
        context = {
            'program': program,
            'members': ProgramMember.objects.filter(Q(role='Miembro')|Q(role='Coordinador')|Q(role='Secretario'), program=program),
            'scope': 'Comité académico',
        }
    elif scope == 'professors':
        context = {
            'program': program,
            'members': ProgramMember.objects.filter(program=program, role='Profesor'),
            'scope': 'Profesores',
        }
    elif scope == 'tutors':
        context = {
            'program': program,
            'members': ProgramMember.objects.filter(program=program, role='Tutor'),
            'scope': 'Tutores',
        }

    return render(request, 'programs/members_list.html', context)

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
                country=request.POST['student_country'],
                gender=request.POST['gender'],
                dni=request.POST['student_dni'],
                birth_date=request.POST['student_birth_date']

            )
            if 'request_date' in request.POST and not request.POST['request_date'] == '':
                Student.objects.filter(pk=student_id).update(
                    request_date=request.POST['request_date']
                )
            if 'init_date' in request.POST and not request.POST['init_date'] == '':
                Student.objects.filter(pk=student_id).update(
                    init_date=request.POST['init_date']
                )
            if 'graduate_date' in request.POST and not request.POST['graduate_date'] == '':
                Student.objects.filter(pk=student_id).update(
                    graduate_date=request.POST['graduate_date']
                )

            PhdStudent.objects.filter(student=Student.objects.get(pk=student_id)).update(
                status=request.POST['student_status']
            )

            student_theme, created = PhdStudentTheme.objects.get_or_create(
                phd_student=PhdStudent.objects.get(student=Student.objects.get(pk=student_id)),
            )
            student_theme.description = request.POST['theme']

            student_theme.save()
            try:
                student_theme.project = InvestigationProject.objects.get(pk=request.POST['investigation_project'])
                student_theme.line = InvestigationProject.objects.get(pk=request.POST['investigation_project']).line
                student_theme.save()
            except:
                pass

            try:
                if request.FILES['student_picture']:
                    student=Student.objects.get(pk=student_id)
                    student.picture=request.FILES['student_picture']
                    student.save()
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
            for requirement in ProgramFinishRequirements.objects.filter(program=program):
                if 'student_f_requirement_' + str(requirement.id) in request.POST:
                    s_f_r=StudentFinishRequirement.objects.get(student=Student.objects.get(pk=student_id), requirement=requirement)
                    s_f_r.accomplished=True
                    s_f_r.save()
                else:
                    s_f_r = StudentFinishRequirement.objects.get(student=Student.objects.get(pk=student_id),
                                                                 requirement=requirement)
                    s_f_r.accomplished = False
                    s_f_r.save()

            return HttpResponseRedirect(reverse('programs:students_list', args=[program_slug,'all']))
        else:
            context = {
                'program': program,
                'student': Student.objects.get(pk=student_id),
                'init_requirements': ProgramInitRequirements.objects.filter(program=program),
                'finish_requirements': ProgramFinishRequirements.objects.filter(program=program),
                'projects': InvestigationProject.objects.filter(program=program),
            }
            return render(request, 'programs/edit_phd_student.html', context)
    else:
        return error_500(request,program,'Usted no tiene privilegios para editar estudiantes de este programa.')


def error_500(request, program, error_message):
    context={
        'program':program,
        'error_message':error_message,
    }
    return render(request,'programs/error_500.html', context)

@login_required
def create_professor(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method == 'POST':
            try:
                user = User.objects.get(email=request.POST['email'])
            except User.DoesNotExist:
                passwd = program_slug + str(random.randint(1000000, 9999999))
                user = User.objects.create_user(
                    request.POST['email'],
                    request.POST['email'],
                    passwd,  # Cambiar a password generada luego #
                )
                user.first_name = request.POST['name']
                user.last_name = request.POST['surename']
                user.save()
            try:
                professor=ProgramMember.objects.get(user=user, program=program)
                return error_500(request,program,'Ya existe un profesor con este email en el sistema, verifique que no lo intenta duplicar.')
            except:
                professor = ProgramMember(
                    program=program,
                    user=user,
                    role=request.POST['role'],
                    institution=request.POST['institution'],
                    degree=request.POST['grade'],
                    phone=request.POST['phone'],
                    country=request.POST['country'],
                    fb_contact=request.POST['fb_contact'],
                    tw_contact=request.POST['tw_contact'],
                    ln_contact=request.POST['ln_contact'],
                    sex=request.POST['gender'],
                    birth_date=request.POST['member_birth_date'],


                )
                if professor.role=='Coordinador':
                    professor.weight=1
                elif professor.role=='Secretario':
                    professor.weight=2
                elif professor.role=='Miembro':
                    professor.weight=3
                elif professor.role=='Profesor':
                    professor.weight=4
                elif professor.role=='Tutor':
                    professor.weight=5


                try:
                    professor.save()
                    # send_mail('Hola','Usuario creado',program.email,[professor.user.email,'boris_perez@unah.edu.cu'], fail_silently=False)
                    utils_send_email(request, 'wm', program.email, professor, '', '', program, passwd)
                    try:
                        professor.picture=request.FILES['picture']
                        professor.save()
                    except:
                        pass
                    # TODO: enviar email al profesor creado
                    return HttpResponseRedirect(reverse('programs:members_list',args=[program_slug, 'all']))

                except:
                    if not ProgramMember.objects.filter(user=user) and not Student.objects.filter(user=user):
                        user.delete()
                    return error_500(request, program,
                                     'Una excepción se ha lanzado al tratar de guardar lso datos del nuevo miembro.')

        else:
            context={
                'program':program,

            }
            return render(request, 'programs/create_professor.html', context)

@login_required
def edit_member(request, program_slug, member_id):
    program = Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method == 'POST':
            user=ProgramMember.objects.get(pk=member_id).user
            user.first_name=request.POST['name']
            user.last_name=request.POST['surename']
            user.email=request.POST['email']
            user.save()
            ProgramMember.objects.filter(pk=member_id).update(
                role=request.POST['role'],
                institution=request.POST['institution'],
                degree=request.POST['grade'],
                phone=request.POST['phone'],
                country=request.POST['country'],
                fb_contact=request.POST['fb_contact'],
                tw_contact=request.POST['tw_contact'],
                ln_contact=request.POST['ln_contact'],
                sex=request.POST['gender'],
                birth_date=request.POST['member_birth_date'],
            )
            professor=ProgramMember.objects.get(pk=member_id)
            if request.POST['role'] == 'Coordinador':
                professor.weight = 1
            elif request.POST['role'] == 'Secretario':
                professor.weight = 2
            elif request.POST['role'] == 'Miembro':
                professor.weight = 3
            elif request.POST['role'] == 'Profesor':
                professor.weight = 4
            elif request.POST['role'] == 'Tutor':
                professor.weight = 5
            professor.save()
            try:
                professor.picture=request.FILES['picture']
                professor.save()
            except:
                print('Excepcion sin foto')

            return HttpResponseRedirect(reverse('programs:members_list',args=[program_slug, 'all']))
        else:
            context={
                'program':program,
                'member':ProgramMember.objects.get(pk=member_id)
            }
            return render(request,'programs/edit_professor.html',context)
    else:
        return error_500(request,program,'Usted no tiene privilegios para editar miembros de este programa.')


#Devuelve 0 si el user no existe, 1 si existe pero no es miembro del programa, 2 si existe y es miembro del programa
@login_required
def ajx_usr_exists(request,program_slug):
    program = Program.objects.get(slug=program_slug)

    if request.method=='POST':

        try:
            user= User.objects.get(email=request.POST['email'])
            if user_is_program_member(user, program ):
                return HttpResponse(
                    json.dumps([{'exists': 2}]),
                    content_type="application/json"
                )
            else:
                return HttpResponse(
                    json.dumps([{'exists': 1}]),
                    content_type="application/json"
                )


        except User.DoesNotExist:
            return HttpResponse(
                json.dumps([{'exists': 0}]),
                content_type="application/json"
            )
    else:
        return HttpResponse(
            json.dumps([{'exists': 0}]),
            content_type="application/json"
        )

@login_required
def create_line(request, program_slug):
    program= Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user,program):
        if request.method=='POST':
            new_line = InvestigationLine(
                program=program,
                name=request.POST['line_name']
            )
            new_line.save()
            return HttpResponseRedirect(reverse('programs:program_lines', args=[program_slug]))

        else:
            context={
                'program':program,
            }
            return render(request, 'programs/create_line.html', context)
    else:
        return error_500(request,program,'Usted no tiene privilegios para crear líneas.')

@login_required
def edit_line(request, program_slug, line_id):
    program = Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method == 'POST':
            InvestigationLine.objects.filter(pk=line_id).update(
                name=request.POST['line_name']
            )
            return HttpResponseRedirect(reverse('programs:program_lines', args=[program_slug]))
        else:
            context={
                'program':program,
                'line':InvestigationLine.objects.get(pk=line_id),
            }
            return render(request, 'programs/edit_line.html', context)
    else:
        return error_500(request,program,'Usted no tiene privilegios para editar esta linea')




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
def create_project(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method=='POST':
            new_project=InvestigationProject(
                program=program,
                line=InvestigationLine.objects.get(pk=request.POST['line']),
                name=request.POST['project_name'],
                institution=request.POST['project_institution'],
                init_date=request.POST['project_init_date'],
                end_date=request.POST['project_end_date'],
            )
            new_project.save()
            return HttpResponseRedirect(reverse('programs:projects_list', args=[program_slug]))
        else:
            context={
                'program':program,
                'lines':InvestigationLine.objects.filter(program=program),
            }
            return render(request, 'programs/create_project.html', context)
    else:
        return error_500(request,program,'Usted no tiene proivilegios para crear proyectos')


@login_required
def projects_list(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    context={
        'program':program,
        'projects':InvestigationProject.objects.filter(program=program)
    }
    return render(request, 'programs/projects_list.html',context)

@login_required
def edit_project(request, program_slug, project_id):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        if request.method=='POST':
            InvestigationProject.objects.filter(pk=project_id).update(
                line=InvestigationLine.objects.get(pk=request.POST['line']),
                name=request.POST['project_name'],
                institution=request.POST['project_institution'],
                init_date=request.POST['project_init_date'],
                end_date=request.POST['project_end_date'],
            )

            return HttpResponseRedirect(reverse('programs:projects_list', args=[program_slug]))
        else:
            context={
                'program':program,
                'lines':InvestigationLine.objects.filter(program=program),
                'project':  InvestigationProject.objects.get(pk=project_id),
            }
            return render(request, 'programs/edit_project.html', context)
    else:
        return error_500(request,program,'Usted no tiene privilegios para editar proyectos')

@login_required
def ajx_delete_student(request, program_slug):
    program=Program.objects.get(slug=program_slug)

    if user_is_program_cs(request.user,program ):
        if request.method=='POST':
            student_id=request.POST['student_id']
            try:
                Student.objects.get(pk=student_id).delete()
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
def ajx_delete_line(request, program_slug):
    program=Program.objects.get(slug=program_slug)

    if user_is_program_cs(request.user,program ):
        if request.method=='POST':
            line_id=request.POST['line_id']
            try:
                InvestigationLine.objects.get(pk=line_id).delete()
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
def ajx_delete_project(request, program_slug):
    program=Program.objects.get(slug=program_slug)

    if user_is_program_cs(request.user,program ):
        if request.method=='POST':
            project_id=request.POST['project_id']
            try:
                InvestigationProject.objects.get(pk=project_id).delete()
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
def ajx_this_year_requests(request, program_slug):
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


@login_required
def ajx_by_year_requests(request, program_slug):
    year=request.POST['year']
    response_data=[]
    labels = []
    data = []
    data_1=[]
    data_2=[]
    meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
             8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for i in range(1,13):
        labels.append(meses[i])
        data_1.append(Student.objects.filter(request_date__year=year,request_date__month=i).__len__())
        data_2.append(Student.objects.filter(init_date__year=year,init_date__month=i).__len__())

    data.append(data_1)
    data.append(data_2)

    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_last_years_requests(request, program_slug):
    response_data=[]
    labels = []
    data = []
    data_1=[]
    data_2=[]

    # locale.setlocale(locale.LC_ALL, 'es-ES')

    for i in range(now().year-4,now().year+1):
        labels.append(i)
        data_1.append(Student.objects.filter(request_date__year=i).__len__())
        data_2.append(Student.objects.filter(init_date__year=i).__len__())

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
    response_data=[]
    labels = []
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    for line in InvestigationLine.objects.filter(program=Program.objects.get(slug=program_slug)):
        i += 1
        labels.append(line.name.split()[0])
        data.append(PhdStudentTheme.objects.filter(line=line).__len__())


    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

@login_required
def ajx_students_by_age(request, program_slug):
    response_data=[]
    labels = ['<30 años','30-40','40-50','>50 años']
    data = []

    # locale.setlocale(locale.LC_ALL, 'es-ES')
    i=0
    data.append(Student.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-30 ).__len__())
    data.append(Student.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-40, birth_date__year__lt=now().year-30 ).__len__() )
    data.append(Student.objects.filter(program=Program.objects.get(slug=program_slug ),birth_date__year__gt=now().year-50, birth_date__year__lt=now().year-40 ).__len__() )
    data.append(Student.objects.filter(program=Program.objects.get(slug=program_slug ), birth_date__year__lt=now().year-50 ).__len__() )


    response_data.append(labels)
    response_data.append(data)


    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

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
def ajx_students_by_state(request, program_slug):
    response_data=[]
    program=Program.objects.get(slug=program_slug)
    response_data.append(PhdStudent.objects.filter(student__program=program, status='Graduado').__len__())
    response_data.append(PhdStudent.objects.filter(student__program=program, status='Solicitante').__len__())
    response_data.append(PhdStudent.objects.filter(student__program=program, status='Doctorando').__len__())
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
    response_data.append(PhdStudent.objects.filter(student__program=program, student__gender='f').__len__())
    response_data.append(PhdStudent.objects.filter(student__program=program, student__gender='m').__len__())
    return HttpResponse(
        json.dumps(response_data),
        content_type="application/json"
    )

def program_member_picture(request, program_slug, member_id):
    fs = FileSystemStorage()
    # filename = Papers.objects.get(pk=paper_id).file_url +  str(Papers.objects.get(pk=paper_id).file)
    filename = ProgramMember.objects.get(pk=member_id).picture.url
    if fs.exists(filename):
        with fs.open(filename) as img:
            response = HttpResponse(img, content_type='image/jpeg')
            return response
    else:
        return HttpResponse('Error')

def program_student_picture(request, program_slug, student_id):
    fs = FileSystemStorage()
    # filename = Papers.objects.get(pk=paper_id).file_url +  str(Papers.objects.get(pk=paper_id).file)
    filename = Student.objects.get(pk=student_id).picture.url
    if fs.exists(filename):
        with fs.open(filename) as img:
            response = HttpResponse(img, content_type='image/jpeg')
            return response
    else:
        return HttpResponse('Error')

def program_background(request, program_slug, background_id):
    fs = FileSystemStorage()
    # filename = Papers.objects.get(pk=paper_id).file_url +  str(Papers.objects.get(pk=paper_id).file)
    filename = ProgramBackgrounds.objects.get(pk=background_id).background.url
    if fs.exists(filename):
        with fs.open(filename) as img:
            response = HttpResponse(img, content_type='image/jpeg')
            return response
    else:
        return HttpResponse('Error')

@login_required
def program_statistics(request, program_slug):
    program=Program.objects.get(slug=program_slug)
    if user_is_program_cs(request.user, program):
        context={
            'program':program,
        }
        return render(request, 'programs/statistics.html', context)