from programs.models import ProgramMember


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
