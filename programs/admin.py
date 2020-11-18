from django.contrib import admin

from programs.models import InvestigationLine, Student, MscStudent, Tuthor, StudentFormationPlan, InnerAreas, \
    PhdStudent, DipStudent, PostgMember, ProgramSpeciality, New
from .models import Program, CGC_Member, ProgramFinishRequirements, ProgramInitRequirements, ProgramBackgrounds, ProgramMember, ProgramFileDoc

# Register your models here.

class ProgramFileDocInline(admin.TabularInline):
    model = ProgramFileDoc
    extra = 3


class ProgramBackgroundsInline(admin.StackedInline):
    model = ProgramBackgrounds
    extra = 3

class ProgramSpecialityInline(admin.StackedInline):
    model = ProgramSpeciality
    extra = 3

class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}
    list_display = ('full_name','short_name','type')
    inlines = [ProgramFileDocInline, ProgramBackgroundsInline, ProgramSpecialityInline ]

admin.site.register(Program, ProgramAdmin)

class CGC_MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'charge')

admin.site.register(CGC_Member, CGC_MemberAdmin)

class ProgramMemberAdmin(admin.ModelAdmin):
    list_display = ['user','program','role','weight']

admin.site.register(ProgramMember, ProgramMemberAdmin)

class PhdStudentAdmin(admin.ModelAdmin):
    list_display = ('student','status', 'category')

class NewAdmin(admin.ModelAdmin):
    list_display = ['program','date', 'title', ]


admin.site.register(New, NewAdmin)

admin.site.register(PhdStudent, PhdStudentAdmin)

admin.site.register(InvestigationLine)

admin.site.register(MscStudent)
admin.site.register(DipStudent)
admin.site.register(Tuthor)
admin.site.register(InnerAreas)

class PostgMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'charge']

admin.site.register(PostgMember, PostgMemberAdmin)