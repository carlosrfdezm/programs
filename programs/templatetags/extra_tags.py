import string

import math
from django import template
from django.contrib.auth.models import User
from math import floor

from django.db.models import Q
from django.utils.timezone import now

from programs.models import ProgramInitRequirements, StudentInitRequirement, ProgramMember, StudentFinishRequirement, \
    ProgramFinishRequirements, CGC_Member, PhdStudent, PhdStudentTheme, InvestigationProject, Student, \
    StudentFormationPlan, MscStudent, DipStudent, StudentFileDocument, ProgramFileDoc

register = template.Library()

@register.simple_tag
def country_list():
    return ["Afganistán", "Akrotiri", "Albania", "Alemania", "Andorra", "Angola", "Anguila", "Antártida",
            "Antigua y Barbuda", "Antillas Neerlandesas", "Arabia Saudí", "Arctic Ocean", "Argelia", "Argentina",
            "Armenia", "Aruba", "Ashmore andCartier Islands", "Atlantic Ocean", "Australia", "Austria", "Azerbaiyán",
            "Bahamas", "Bahráin", "Bangladesh", "Barbados", "Bélgica", "Belice", "Benín", "Bermudas", "Bielorrusia",
            "Birmania Myanmar", "Bolivia", "Bosnia y Hercegovina", "Botsuana", "Brasil", "Brunéi", "Bulgaria", "Burkina Faso",
            "Burundi", "Bután", "Cabo Verde", "Camboya", "Camerún", "Canadá", "Chad", "Chile", "China", "Chipre", "Clipperton Island",
            "Colombia", "Comoras", "Congo", "Coral Sea Islands", "Corea del Norte", "Corea del Sur", "Costa de Marfil", "Costa Rica",
            "Croacia", "Cuba", "Dhekelia", "Dinamarca", "Dominica", "Ecuador", "Egipto", "El Salvador", "El Vaticano",
            "Emiratos Árabes Unidos", "Eritrea", "Eslovaquia", "Eslovenia", "España", "Estados Unidos", "Estonia",
            "Etiopía", "Filipinas", "Finlandia", "Fiyi", "Francia", "Gabón", "Gambia", "Gaza Strip", "Georgia", "Ghana",
            "Gibraltar", "Granada", "Grecia", "Groenlandia", "Guam", "Guatemala", "Guernsey", "Guinea", "Guinea Ecuatorial",
            "Guinea-Bissau", "Guyana", "Haití", "Honduras", "Hong Kong", "Hungría", "India", "Indian Ocean", "Indonesia", "Irán",
            "Iraq", "Irlanda", "Isla Bouvet", "Isla Christmas", "Isla Norfolk", "Islandia", "Islas Caimán", "Islas Cocos",
            "Islas Cook", "Islas Feroe", "Islas Georgia del Sur y Sandwich del Sur", "Islas Heard y McDonald", "Islas Malvinas",
            "Islas Marianas del Norte", "IslasMarshall", "Islas Pitcairn", "Islas Salomón", "Islas Turcas y Caicos",
            "Islas Vírgenes Americanas", "Islas Vírgenes Británicas", "Israel", "Italia", "Jamaica", "Jan Mayen",
            "Japón", "Jersey", "Jordania", "Kazajistán", "Kenia", "Kirguizistán", "Kiribati", "Kuwait", "Laos", "Lesoto",
            "Letonia", "Líbano", "Liberia", "Libia", "Liechtenstein", "Lituania", "Luxemburgo", "Macao", "Macedonia",
            "Madagascar", "Malasia", "Malaui", "Maldivas", "Malí", "Malta", "Man, Isle of", "Marruecos", "Mauricio",
            "Mauritania", "Mayotte", "México", "Micronesia", "Moldavia", "Mónaco", "Mongolia", "Montserrat",
            "Mozambique", "Namibia", "Nauru", "Navassa Island", "Nepal", "Nicaragua", "Níger", "Nigeria", "Niue",
            "Noruega", "Nueva Caledonia", "Nueva Zelanda", "Omán", "Pacific Ocean", "Países Bajos", "Pakistán", "Palaos",
            "Panamá", "Papúa-Nueva Guinea", "Paracel Islands", "Paraguay", "Perú", "Polinesia Francesa", "Polonia", "Portugal",
            "Puerto Rico", "Qatar", "Reino Unido", "República Centroafricana", "República Checa", "República Democrática del Congo",
            "República Dominicana", "Ruanda", "Rumania", "Rusia", "Sáhara Occidental", "Samoa", "Samoa Americana", "San Cristóbal y Nieves",
            "San Marino", "San Pedro y Miquelón", "San Vicente y las Granadinas", "Santa Helena", "Santa Lucía", "Santo Tomé y Príncipe",
            "Senegal", "Seychelles", "Sierra Leona", "Singapur", "Siria", "Somalia", "Southern Ocean", "Spratly Islands", "Sri Lanka",
            "Suazilandia", "Sudáfrica", "Sudán", "Suecia", "Suiza", "Surinam", "Svalbard y Jan Mayen", "Tailandia", "Taiwán",
            "Tanzania", "Tayikistán", "TerritorioBritánicodel Océano Indico", "Territorios Australes Franceses",
            "Timor Oriental", "Togo", "Tokelau", "Tonga", "Trinidad y Tobago", "Túnez", "Turkmenistán", "Turquía",
            "Tuvalu", "Ucrania", "Uganda", "Unión Europea", "Uruguay",
            "Uzbekistán", "Vanuatu", "Venezuela", "Vietnam", "Wake Island", "Wallis y Futuna",
            "West Bank", "World", "Yemen", "Yibuti", "Zambia", "Zimbabue"]

@register.simple_tag
def init_requirements_accomplished(student, program):
    accomplished=True
    if program.type == 'phd':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_init_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(student=student, program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished=False
    elif program.type == 'msc':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_init_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(msc_student=student, program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished = False
    elif program.type == 'dip':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_init_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(msc_student=student,
                                                                                        program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished = False

    return accomplished

@register.simple_tag
def is_past(date):
    if date < now().date():
        return True
    else:
        return False

@register.simple_tag
def finish_requirements_accomplished(student, program):
    accomplished = True
    if program.type == 'phd':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_finish_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(student=student,
                                                                                     program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished = False
    elif program.type == 'msc':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_finish_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(msc_student=student,
                                                                                     program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished = False
    elif program.type == 'dip':
        for requirement in ProgramFileDoc.objects.filter(program=program, is_finish_requirenment=True):
            student_requirement, created = StudentFileDocument.objects.get_or_create(msc_student=student,
                                                                                     program_file_document=requirement)
            if not student_requirement.accomplished:
                accomplished = False


    return accomplished


@register.simple_tag
def student_init_requirement_accomplished(student, program_requirement):
    if program_requirement.program.type == 'phd':
        student_requirement, created=StudentInitRequirement.objects.get_or_create(student=student, requirement=program_requirement)
    elif program_requirement.program.type == 'msc':
        student_requirement, created=StudentInitRequirement.objects.get_or_create(msc_student=student, requirement=program_requirement)

    if student_requirement.accomplished:
        return True
    else:
        return False

@register.simple_tag
def student_doc_caducity_date(student, program_document):
    if program_document.get_old:
        if program_document.program.type == 'phd':
            return StudentFileDocument.objects.get(student=student, program_file_document=program_document).caducity_date
        elif program_document.program.type == 'msc':
            return StudentFileDocument.objects.get(msc_student=student, program_file_document=program_document).caducity_date
        elif program_document.program.type == 'dip':
            return StudentFileDocument.objects.get(dip_student=student, program_file_document=program_document).caducity_date
    else:
        return None

@register.simple_tag
def student_doc_has_file(student, program_requirement):
    program = program_requirement.program
    if program.type == 'phd':
        try:
            student_doc = StudentFileDocument.objects.get(student=student, program_file_document=program_requirement)
        except StudentFileDocument.DoesNotExist:
            student_doc = StudentFileDocument(
                student=student,
                program_file_document=program_requirement,
            )
            student_doc.save()

            return False



    elif program.type == 'msc':
        try:
            student_doc = StudentFileDocument.objects.get(msc_student=student, program_file_document=program_requirement)
        except StudentFileDocument.DoesNotExist:
            student_doc = StudentFileDocument(
                msc_student=student,
                program_file_document=program_requirement,
            )
            student_doc.save()

            return False
    elif program.type == 'dip':
        try:
            student_doc = StudentFileDocument.objects.get(dip_student=student, program_file_document=program_requirement)
        except StudentFileDocument.DoesNotExist:
            student_doc = StudentFileDocument(
                dip_student=student,
                program_file_document=program_requirement,
            )
            student_doc.save()

            return False

    if student_doc.file:
        return True
    else:
        return False


@register.simple_tag
def student_requirement_accomplished(student, program_requirement):
    if program_requirement.program.type == 'phd':
        student_requirement, created=StudentFileDocument.objects.get_or_create(student=student, program_file_document=program_requirement)
    elif program_requirement.program.type == 'msc':
        student_requirement, created=StudentFileDocument.objects.get_or_create(msc_student=student, program_file_document=program_requirement)
    elif program_requirement.program.type == 'dip':
        student_requirement, created=StudentFileDocument.objects.get_or_create(dip_student=student, program_file_document=program_requirement)

    if student_requirement.accomplished:
        return True
    else:
        return False


@register.simple_tag
def student_finish_requirement_accomplished(student, program_requirement):
    if program_requirement.program.type == 'phd':
        student_requirement, created=StudentFinishRequirement.objects.get_or_create(student=student, requirement=program_requirement)
    elif program_requirement.program.type == 'msc':
        student_requirement, created = StudentFinishRequirement.objects.get_or_create(msc_student=student,
                                                                                      requirement=program_requirement)

    if student_requirement.accomplished:
        return True
    else:
        return False

@register.simple_tag
def program_has_init_requirenments(program):
    if ProgramFileDoc.objects.filter(program=program, is_init_requirenment=True):
        return True
    else:
        return False

@register.simple_tag
def program_has_finish_requirenments(program):
    if ProgramFileDoc.objects.filter(program=program, is_finish_requirenment=True):
        return True
    else:
        return False

@register.simple_tag
def program_has_other_requirenments(program):
    if ProgramFileDoc.objects.filter(program=program, is_init_requirenment=False, is_finish_requirenment=False):
        return True
    else:
        return False



@register.simple_tag
def student_has_init_requirement_pending(student, program):
    has_pending = False
    if program.type == 'phd':
        for requirement in StudentFileDocument.objects.filter(student=student, program_file_document__is_init_requirenment=True):
            if not requirement.accomplished:
                has_pending=True
    elif program.type == 'msc':
        for requirement in StudentFileDocument.objects.filter(msc_student=student, program_file_document__is_init_requirenment=True):
            if not requirement.accomplished:
                has_pending=True

    return has_pending




@register.simple_tag
def user_is_program_cs(user, program):
    try:
        member=ProgramMember.objects.get(user=user, program=program)
        if member.role == 'Coordinador' or member.role == 'Secretario':
            return True
        else:
            return False

    except:
        return False

@register.simple_tag
def sender_program_member(sender, program):
    return  ProgramMember.objects.get(user=sender, program=program)

@register.simple_tag
def sender_program_student(sender, program):
    if program.type == 'phd':
        return  Student.objects.get(user=sender, program=program)
    elif program.type == 'msc':
        return  MscStudent.objects.get(user=sender, program=program)
    elif program.type == 'dip':
        return  DipStudent.objects.get(user=sender, program=program)

@register.simple_tag
def user_is_program_member(user, program):
    try:
        member=ProgramMember.objects.get(user=user, program=program)
        return True
    except ProgramMember.DoesNotExist:
        return False

@register.simple_tag
def user_is_program_student(user, program):
    if program.type == 'phd':
        try:
            student=Student.objects.get(user=user, program=program)
            return True
        except:
            return False
    elif program.type == 'msc':
        try:
            student=MscStudent.objects.get(user=user, program=program)
            return True
        except:
            return False
    elif program.type == 'dip':
        try:
            student=DipStudent.objects.get(user=user, program=program)
            return True
        except:
            return False


@register.simple_tag
def user_is_cgc_ps(user):
    try:
        member=CGC_Member.objects.get(user=user)
        if member.charge == 'Presidente' or member.charge == 'Secretario':
            return True
        else:
            return False

    except:
        return False

@register.simple_tag
def student_has_activities(student):
    try:
        formation_plan = StudentFormationPlan.objects.get(phdstudent=student)
        if formation_plan.formationplanactivities_set.all().__len__() > 0:
            return True
        else:
            return False
    except StudentFormationPlan.DoesNotExist:
        return False

@register.simple_tag
def max_year_birth_date():
    return now().year-20

#Devuelve la lista de programas a los que pertenece un usuario (como miembro)
@register.simple_tag
def user_programs_member(user):
    programs=[]
    for member in ProgramMember.objects.filter(user=user):
        if not member.program in programs and member.program.type == 'phd':
            programs.append(member.program)
        else:
            pass

    return programs

@register.simple_tag
def user_programs_comite_member(user):
    programs=[]
    for member in ProgramMember.objects.filter(Q(role='Coordinador')|Q(role='Secretario')|Q(role='Miembro'),user=user):
        if not member.program in programs and member.program.type == 'phd':
            programs.append(member.program)
        else:
            pass

    return programs

@register.simple_tag
def program_requesters(program):
    if program.type == 'phd':
        return PhdStudent.objects.filter(status='solicitante', student__program=program).__len__()
    elif program.type == 'msc':
        return MscStudent.objects.filter(status='solicitante', program=program).__len__()
    elif program.type == 'dip':
        return DipStudent.objects.filter(status='solicitante', program=program).__len__()
    else:
        return 'Error'

@register.simple_tag
def program_aproved(program):
    if program.type == 'phd':
        return PhdStudent.objects.filter(status='doctorando', student__program=program).__len__()
    elif program.type == 'msc':
        return MscStudent.objects.filter(status='maestrante', program=program).__len__()
    elif program.type == 'dip':
        return DipStudent.objects.filter(status='diplomante', program=program).__len__()
    else:
        return 'Error'

@register.simple_tag
def program_graduated(program):
    if program.type == 'phd':
        return PhdStudent.objects.filter(status='graduado', student__program=program).__len__()
    elif program.type == 'msc':
        return MscStudent.objects.filter(status='graduado', program=program).__len__()
    elif program.type == 'dip':
        return DipStudent.objects.filter(status='graduado', program=program).__len__()
    else:
        return 'Error'

@register.simple_tag
def project_students(project):
    return PhdStudentTheme.objects.filter(project=project).__len__()

@register.simple_tag
def line_projects(line):
    return InvestigationProject.objects.filter(line=line).__len__()

@register.simple_tag
def program_has_coordinator(program):
    if ProgramMember.objects.filter(program=program, role='coordinador'):
        return True
    else:
        return False

@register.simple_tag
def program_has_secretary(program):
    if ProgramMember.objects.filter(program=program, role='secretario'):
        return True
    else:
        return False

@register.simple_tag
def current_year():
    return now().year

@register.simple_tag
def five_years_ahead():
    return now().year+5
