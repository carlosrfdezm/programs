from django.contrib import admin
from .models import Program, CGC_Member, ProgramFinishRequirements, ProgramInitRequirements

# Register your models here.

class ProgramAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("short_name",)}
    list_display = ('full_name','short_name','type')

admin.site.register(Program, ProgramAdmin)

class CGC_MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'charge')

admin.site.register(CGC_Member, CGC_MemberAdmin)

admin.site.register(ProgramInitRequirements)

admin.site.register(ProgramFinishRequirements)
