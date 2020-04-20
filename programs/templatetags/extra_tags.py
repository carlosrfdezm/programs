import string

import math
from django import template
from django.contrib.auth.models import User
from math import floor

from django.db.models import Q
from django.utils.timezone import now

from programs.models import ProgramInitRequirements, StudentInitRequirement, ProgramMember, StudentFinishRequirement, \
    ProgramFinishRequirements, CGC_Member, PhdStudent

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
        for requirement in ProgramInitRequirements.objects.filter(program=program):
            for student_requirement in StudentInitRequirement.objects.filter(requirement__program=program, student=student):
                if not student_requirement.accomplished:
                    accomplished=False
    elif program.type == 'msc':
        for requirement in ProgramInitRequirements.objects.filter(program=program):
            for student_requirement in StudentInitRequirement.objects.filter(requirement__program=program, msc_student=student):
                if not student_requirement.accomplished:
                    accomplished=False


    return accomplished

@register.simple_tag
def finish_requirements_accomplished(student, program):
    accomplished=True
    if program.type == 'phd':
        for requirement in ProgramFinishRequirements.objects.filter(program=program):
            for student_requirement in StudentFinishRequirement.objects.filter(requirement__program=program, student=student):
                if not student_requirement.accomplished:
                    accomplished=False
    elif program.type == 'msc':
        for requirement in ProgramFinishRequirements.objects.filter(program=program):
            for student_requirement in StudentFinishRequirement.objects.filter(requirement__program=program, msc_student=student):
                if not student_requirement.accomplished:
                    accomplished=False


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
def user_is_cgc_ps(user):
    try:
        member=CGC_Member.objects.get(user=user)
        if member.role == 'Presidente' or member.role == 'Secretario':
            return True
        else:
            return False

    except:
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
    else:
        return 'Error'

@register.simple_tag
def program_aproved(program):
    if program.type == 'phd':
        return PhdStudent.objects.filter(status='doctorando', student__program=program).__len__()
    else:
        return 'Error'

@register.simple_tag
def program_graduated(program):
    if program.type == 'phd':
        return PhdStudent.objects.filter(status='graduado', student__program=program).__len__()
    else:
        return 'Error'


