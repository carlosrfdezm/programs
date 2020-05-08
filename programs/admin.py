from django.contrib import admin

from programs.models import InvestigationLine, Student, MscStudent, Tuthor
from .models import Program, CGC_Member, ProgramFinishRequirements, ProgramInitRequirements, ProgramBackgrounds, ProgramMember

# Register your models here.

class ProgramInitRequirementsInline(admin.TabularInline):
    model = ProgramInitRequirements
    extra = 1

class ProgramFinishRequirementsInline(admin.TabularInline):
    model = ProgramFinishRequirements
    extra = 1

class ProgramBackgroundsInline(admin.StackedInline):
    model = ProgramBackgrounds
    extra = 3

class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}
    list_display = ('full_name','short_name','type')
    inlines = [ProgramInitRequirementsInline, ProgramFinishRequirementsInline, ProgramBackgroundsInline ]

admin.site.register(Program, ProgramAdmin)

class CGC_MemberAdmin(admin.ModelAdmin):
    list_display = ('user', 'charge')

admin.site.register(CGC_Member, CGC_MemberAdmin)

class ProgramMemberAdmin(admin.ModelAdmin):
    list_display = ['user','program','role','weight']

admin.site.register(ProgramMember, ProgramMemberAdmin)

admin.site.register(InvestigationLine)
admin.site.register(Student)
admin.site.register(MscStudent)
admin.site.register(Tuthor)