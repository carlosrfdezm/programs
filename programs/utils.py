import random

from django.contrib.auth.models import User

from programs.models import ProgramMember, Student, CGC_Member, Tuthor, MscStudent, DipStudent
from django.core.mail import send_mail
from django.template import loader


def user_is_program_cs(user, program):
    try:
        member=ProgramMember.objects.get(user=user, program=program)
        if member.role=='Coordinador' or member.role=='Secretario':
            return True
        else:
            return False
    except:
        return False

def user_is_program_member(user, program):
    try:
        member=ProgramMember.objects.get(user=user, program=program)
        return True
    except:
        return False

def user_is_program_student(user, program):
    try:
        student=Student.objects.get(user=user, program=program)
        return True
    except:
        return False

def user_is_cgc_member(user):
    try:
        member=CGC_Member.objects.get(user=user)
        return True
    except:
        return False


def user_is_cgc_ps(user):
    try:
        member=CGC_Member.objects.get(user=user)
        if member.charge == 'Presidente' or member.charge == 'Secretario':
            return True
        else:
            return False
    except:
        return False

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

#Los mensajes pueden ser de tipo wm (welcome_message), nc (new court), o custom (enviado por otro miembro)
def utils_send_email(request, type, sender_email, member, subject, body, program, psw):
    if type == 'wm':
        try:
            context = {
                'program': program,
                'member': member,
                'message_type': type,
                'domain': request.META['HTTP_HOST'],
                'protocol': 'http',
                'psw':psw,
            }

            email_template_name = 'programs/emails/default_email.html'

            email = loader.render_to_string(email_template_name, context)

            send_mail("Información " + program.full_name, email, program.email, [member.user.email],fail_silently=False)
        except:
            pass


# En este caso type debe ser request_received o request_confirmed. Es request received cdo se crea el requester
# y es de tipo request_confirmed cuando esa solicitud se confirma
def request_send_email(request, type, requester, program):
    if type == 'request_received':
        try:
            context = {
                'program': program,
                'requester': requester,
                'message_type': type,
                'domain': request.META['HTTP_HOST'],
                'protocol': 'https',

            }

            email_template_name = 'programs/emails/requester_email.html'

            email = loader.render_to_string(email_template_name, context)

            send_mail("Solicitud de ingreso a " + program.full_name, email, program.email, [requester.email],fail_silently=False)
        except:
            pass

def create_new_tuthor(request, program, first_name,last_name,institution, email,student):
    success=[]
    try:
        user = User.objects.get(username=email)
        try:
            member=ProgramMember.objects.get(user=user, program=program)
            if program.type == 'phd':
                new_tuthor = Tuthor(
                    phd_student=student,
                    professor=member,
                )
                new_tuthor.save()
                success.append(True)
                success.append(new_tuthor.id)
                return success
            elif program.type == 'msc':
                new_tuthor = Tuthor(
                    msc_student=student,
                    professor=member,
                )
                new_tuthor.save()
                success.append(True)
                success.append(new_tuthor.id)
                return success

        except ProgramMember.DoesNotExist:
            new_member = ProgramMember(
                user=user,
                program=program,
                institution=institution,

            )
            new_member.save()
            if program.type == 'phd':
                new_tuthor = Tuthor(
                    phd_student=student,
                    professor=new_member,
                )
                new_tuthor.save()
                success.append(True)
                success.append(new_tuthor.id)
                return success
            elif program.type == 'msc':
                new_tuthor = Tuthor(
                    msc_student=student,
                    professor=new_member,
                )
                new_tuthor.save()
                success.append(True)
                success.append(new_tuthor.id)
                return success


    except User.DoesNotExist:
        passwd = program.slug + str(random.randint(1000000, 9999999))
        user = User.objects.create_user(
            email,
            email,
            passwd,  # Cambiar despues por contrase;a generada

        )
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        new_member = ProgramMember(
            user=user,
            program=program,
            institution=institution,

        )
        new_member.save()

        if program.type == 'phd':
            new_tuthor = Tuthor(
                phd_student=student,
                professor=new_member,
            )
            new_tuthor.save()
            utils_send_email(request, 'wm', program.email, student, '', '', program, passwd)
            success.append(True)
            success.append(new_tuthor.id)
            return success
        elif program.type == 'msc':
            new_tuthor = Tuthor(
                msc_student=student,
                professor=new_member,
            )
            new_tuthor.save()
            utils_send_email(request, 'wm', program.email, student, '', '', program, passwd)
            success.append(True)
            success.append(new_tuthor.id)
            return success


