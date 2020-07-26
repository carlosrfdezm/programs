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
