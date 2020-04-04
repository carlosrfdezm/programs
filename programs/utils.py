from programs.models import ProgramMember
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

#Los mensajes pueden ser de tipo wm (welcome_message), nc (new court), o custom (enviado por otro miembro)
def utils_send_email(request, type, sender_email, member, subject, body, court, psw):
    if type == 'wm':
        try:
            context = {
                'court': court,
                'member': member,
                'message_type': type,
                'domain': request.META['HTTP_HOST'],
                'protocol': 'http',
                'psw':psw,
            }

            email_template_name = 'progrems/emails/default_email.html'

            email = loader.render_to_string(email_template_name, context)


            send_mail("Información " + court.name, email, court.email, ['boris_perez@unah.edu.cu'],fail_silently=False)
        except:
            pass
