from programs.models import ProgramMember


def user_is_program_cs(user, program):
    try:
        member=ProgramMember.objects.get(user=user)
        if member.role=='Coordinador' or member.role=='Secretario':
            return True
        else:
            return False
    except:
        return False
