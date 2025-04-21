from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.text import slugify
from django.utils.timezone import now

from programas import settings
from programas.settings import INSTITUTION_SHORT_NAME, INSTITUTION_FULL_NAME, INSTITUTION_ADDRESS, INSTITUTION_PHONE


def program_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/imgs/{1}'.format(instance.slug, filename)

def program_new_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/news/{1}/{2}'.format(instance.program.slug, instance.id, filename)

def program_brief_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    brief_ext = filename.split('.')[filename.split('.').__len__() - 1].lower
    index = ProgramBrief.objects.filter(program=instance.program, year=instance.year, month=instance.month).__len__()
    if index == 0:
        new_brief_name = 'Acta-' + slugify(instance.program.short_name) + '-'+ instance.month +'-'+ instance.year + '-1.' + brief_ext
    elif index > 0:
        new_brief_name = 'Acta-' + slugify(instance.program.short_name) + '-'+ instance.month +'-' + instance.year + '-'+str(index+1)+ '.' + brief_ext

    return 'program_{0}/brieffings/{1}/{2}/{3}'.format(instance.program.slug, instance.year,
                                                       instance.month, new_brief_name)

def program_document_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    doc_ext = str(filename.split('.')[filename.split('.').__len__() - 1]).lower()
    index = ProgramBrief.objects.filter(program=instance.program, year=instance.year, month=instance.month).__len__()
    new_doc_name = '{0}-{1}-{2}-{3}-{4}.{5}'.format(instance.type.capitalize(),instance.program.slug, instance.month , instance.year ,str(index+1), doc_ext)

    return 'program_{0}/documents/{1}/{2}/{3}'.format(instance.program.slug, instance.year,instance.month, new_doc_name)

def postg_document_path(instance, filename):
    file_ext = str(filename.split('.')[filename.split('.').__len__() - 1]).lower()
    file_name = '{0}_{1}_{2}.{3}'.format(instance.type.capitalize() , instance.year,instance.month, file_ext)

    return 'postg/docs/{0}/{1}'.format(instance.year, file_name)

def formation_document_path(instance, filename):
    file_ext = str(filename.split('.')[filename.split('.').__len__() - 1]).lower()
    file_name = '{0}_{1}_{2}.{3}'.format(instance.type.capitalize() , instance.year,instance.month, file_ext)

    return 'formation/docs/{0}/{1}'.format(instance.year, file_name)


def member_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/members/{1}/{2}'.format(instance.program.slug,instance.id, filename)

def postg_member_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/postg/members/<member_id>/<filename>
    return 'postg/members/{0}/{1}'.format(instance.id, filename)

def formation_member_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/postg/members/<member_id>/<filename>
    return 'formation/members/{0}/{1}'.format(instance.id, filename)

def student_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/students/{1}/{2}'.format(instance.program.slug,instance.id, filename)

def student_filedoc_directory_path(instance, filename):
    program = instance.program_file_document.program
    if program.type == 'phd':
        student = instance.student
    elif program.type == 'msc':
        student = instance.msc_student
    elif program.type == 'dip':
        student = instance.dip_student
    elif program.type == 'curs':
        student = instance.curs_student
    elif program.type == 'coleg':
        student = instance.coleg_student

    # file will be uploaded to MEDIA_ROOT/program_<slug>/students/<student_id>/docs/<filename>
    return 'program_{0}/students/{1}/docs/{2}'.format(program.slug,student.id, filename)

def phd_thesis_directory_path(instance, filename):
    program = instance.phd_student.student.program
    return 'program_{0}/students/{1}/docs/thesis/{2}'.format(program.slug, instance.phd_student.student.id, filename)

def background_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/imgs/backgrounds/{1}'.format(instance.program.slug, filename)

def cgc_photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cgc/imgs/<filename>
    return 'cgc/imgs/{0}'.format(filename)

def cgc_brief_path(instance, filename):
    return 'cgc/brieffings/{0}/{1}/{2}'.format(instance.year,instance.month,filename)

def cgc_doc_path(instance, filename):
    file_ext =str( filename.split('.')[filename.split('.').__len__() - 1]).lower()
    file_name = 'CGC_{0}_{1}_{2}.{3}'.format(instance.type.capitalize(), instance.year, instance.month, file_ext)
    return 'cgc/docs/{0}/{1}/{2}'.format(instance.year,instance.month,file_name)

def cngc_brief_path(instance, filename):
    return 'cngc/brieffings/{0}/{1}/{2}'.format(instance.year,instance.month,filename)

# Create your models here.



ICON_CHOICES = (
    ('ion-ios-alarm-outline', 'ion-ios-alarm-outline'),
    ('ion-ios-albums-outline', 'ion-ios-albums-outline'),
    ('ion-ios-barcode-outline', 'ion-ios-barcode-outline'),
    ('ion-ios-body-outline', 'ion-ios-body-outline'),
    ('ion-ios-book-outline', 'ion-ios-book-outline'),
    ('ion-ios-calculator-outline', 'ion-ios-calculator-outline'),
    ('ion-ios-cloudy-outline', 'ion-ios-cloudy-outline'),
    ('ion-ios-medical-outline', 'ion-ios-medical-outline'),
)

# modelo de programas academicos
class Program(models.Model):
    full_name=models.CharField(max_length=150, help_text='Nombre completo del programa', verbose_name='Nombre completo')
    short_name=models.CharField(max_length=40, help_text='Nombre corto del programa', verbose_name='Nombre Corto')
    description=models.TextField(max_length=200, help_text='Breve descripcion del programa', verbose_name='Descripcion')
    type=models.CharField(max_length=20,choices=[('phd','Doctorado'),('msc','Maestría'),('dip','Diplomado'),('curs', 'Cursos'), ('coleg', 'Colegio')], verbose_name='Tipo')
    branch=models.CharField(max_length=20,default='CP',choices=[('CT','Ciencias Técnicas'),('CE','Ciencias Económicas'),
                                                   ('CNE','Ciencias Naturales y Exactas'),('CA','Ciencias Agrícolas'),
                                                   ('CSH','Ciencias Sociales y Humanísticas'),('CP','Ciencias Pedagógicas'),
                                                   ('Arte','Ciencias del Arte'),('Otros', 'Otros')], verbose_name='Rama del programa')
    code = models.CharField(max_length=10, null=True, blank=True, verbose_name='Codigo del Programa')
    slug=models.SlugField(max_length=40,help_text='Slug para url',unique=True)
    address = models.TextField(max_length=150, help_text='Dirección de la sede del programa')
    phone = models.CharField(max_length=20, help_text='Teléfono de contacto')
    email = models.EmailField(help_text='Email de contacto')
    icon = models.CharField(max_length=100, null=False, blank=False, choices=ICON_CHOICES,
                            help_text='Seleccione una opcion de la lista')
    center = models.CharField(max_length=120, null=True, blank=True)
    self_request = models.BooleanField(default=False, help_text='Marcar si se permite la solicitud al programa desde el sitio')

    class Meta:
        verbose_name = 'Programa'
        verbose_name_plural = 'Programas'

    def __str__(self):
        return self.full_name

class ProgramBackgrounds(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    background = models.ImageField(upload_to=background_directory_path)

    class Meta:
        verbose_name = 'Background'
        verbose_name_plural = 'Backgrounds del index del programa'

# modelo de miembros de la CGC
class CGC_Member(models.Model):
    
    Masculino = 'm'
    Femenino = 'f'
    
    SEX_CHOICES = (
        (Masculino, 'Masculino'),
        (Femenino, 'Femenino'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    charge = models.CharField(max_length=50,choices=[('Presidente','Presidente'),('Director','Director'),('Secretario','Secretario'),('Miembro','Miembro')], help_text='Cargo', verbose_name='Cargo')
    institution= models.CharField(max_length=60,default=INSTITUTION_FULL_NAME)
    priority= models.SmallIntegerField(help_text="Prioridad del Cargo", choices=[(1,'1'),(2,'2'),(3,'3')])
    fb_contact = models.URLField(help_text='URL del contacto de Facebook',default='https://www.facebook.com',  blank=True)
    tw_contact = models.URLField(help_text='URL del contacto de Twitter',default='https://www.twitter.com',  blank=True)
    in_contact = models.URLField(help_text='URL del contacto de Linkedin',default='https://www.linkedin.com',  blank=True)
    gp_contact = models.URLField(help_text='URL del contacto de Google+',default='https://plus.google.com', blank=True)
    picture= models.ImageField(help_text='Foto', upload_to=cgc_photo_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, choices=SEX_CHOICES, help_text='Género')
    phone = models.CharField(max_length=50, null=True, blank=True)
    degree = models.CharField(max_length=100, default='Doctor en Ciencias', help_text='Grado cientifico')
    birth_date = models.DateField(default='1960-01-01', help_text='Fecha de nacimiento')



    class Meta:
        verbose_name = 'Miembro de la CGC'
        verbose_name_plural = 'Miembros de la CGC'

    def __str__(self):
        return self.user.get_full_name()

# modelo de miembros de programas
class ProgramMember(models.Model):

    Masculino = 'm'
    Femenino = 'f'

    ROLE_CHOICES = [
        ('Coordinador', 'Coordinador'),
        ('Secretario', 'Secretario'),
        ('Miembro', 'Miembro'),
        ('Profesor', 'Profesor'),
        ('Tutor', 'Tutor'),

    ]
    SEX_CHOICES = (
        (Masculino, 'Masculino'),
        (Femenino, 'Femenino'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    role = models.CharField(max_length=50,default='Tutor', choices=ROLE_CHOICES)
    country = models.CharField(max_length=70, default='Cuba')
    phone = models.CharField(max_length=50, null=True)
    institution = models.CharField(max_length=100, default=INSTITUTION_SHORT_NAME)
    birth_date = models.DateField(default='1960-01-01', help_text='Fecha de nacimiento')
    degree = models.CharField(max_length=100, default='Doctor en Ciencias de...',
                              help_text='Grado cientifico')
    picture = models.ImageField(null=True, blank=True, upload_to=member_directory_path)
    fb_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Facebook del miembro del tribunal')
    tw_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Twitter del miembro del tribunal')
    ln_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Linkedin del miembro del tribunal')
    init_date = models.DateField(default=now)
    sex = models.CharField(max_length=2,default='m', choices=SEX_CHOICES, help_text='Sexo del miembro del tribunal')
    weight=models.SmallIntegerField(help_text="Peso del Cargo", default=5, choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])

    class Meta:
        verbose_name='Miembro del Programa'
        verbose_name_plural='Miembros del programa'
        ordering=['weight']

    def __str__(self):
        return self.user.get_full_name()

class ProgramSpeciality(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, null=False)
    name = models.CharField(max_length=100, null=False)

    def __str__(self):
        return self.name

class InvestigationLine(models.Model):
    program=models.ForeignKey(Program, on_delete=models.CASCADE)
    name=models.TextField(max_length=500, help_text='Nombre de la linea')

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_date= models.DateField(default=now)
    graduate_date = models.DateField(null=True)
    init_date = models.DateField(null=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')
    is_master = models.BooleanField(default=False)
    msc_title = models.CharField(max_length=100, null=True, blank=True)
    have_prorrogue = models.BooleanField(default=False)
    prorrogue_end_date = models.DateField(null=True, blank=True)
    speciality = models.ForeignKey(ProgramSpeciality, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.user.get_full_name()
    
class StudentOthers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    graduate_date = models.DateField(null=True)
    init_date = models.DateField(null=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')

    def __str__(self):
        return self.user.get_full_name()


    
class ProgramEdition(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    order = models.SmallIntegerField(default=1)
    init_date = models.DateField(default=now)
    end_date = models.DateField()
    observations = models.TextField(max_length=250, null=True)

    def __str__(self):
        return str(self.order)
    
class ColegStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_date= models.DateField(default=now)
    graduate_date = models.DateField(null=True, blank=True)
    init_date = models.DateField(null=True, blank=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')
    status = models.CharField(max_length=15,default='solicitante', choices=[('solicitante', 'Solicitante'), ('estudiante', 'Estudiante'),
                                                                            ('graduado', 'Graduado'), ('denegado', 'Denegado')])
    edition = models.ForeignKey(ProgramEdition, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, default='interno',
                                choices=[('interno', 'Interno'), ('externo', 'Externo')])
    center = models.CharField(max_length=150, default= INSTITUTION_FULL_NAME)

    def __str__(self):
        return self.user.get_full_name()


class MscStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_date= models.DateField(default=now)
    graduate_date = models.DateField(null=True, blank=True)
    init_date = models.DateField(null=True, blank=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')
    status = models.CharField(max_length=15,default='solicitante', choices=[('solicitante', 'Solicitante'), ('maestrante', 'Maestrante'),
                                                                            ('graduado', 'Graduado'), ('denegado', 'Denegado')])
    edition = models.ForeignKey(ProgramEdition, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, default='interno',
                                choices=[('interno', 'Interno'), ('externo', 'Externo')])
    center = models.CharField(max_length=150, default= INSTITUTION_FULL_NAME)

    def __str__(self):
        return self.user.get_full_name()

class DipStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_date= models.DateField(default=now)
    graduate_date = models.DateField(null=True, blank=True)
    init_date = models.DateField(null=True, blank=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')
    status = models.CharField(max_length=15,default='solicitante', choices=[('solicitante', 'Solicitante'), ('diplomante', 'Diplomante'),
                                                                            ('graduado', 'Graduado'), ('denegado', 'Denegado')])
    edition = models.ForeignKey(ProgramEdition, on_delete=models.CASCADE)
    faculty = models.CharField(max_length=100, help_text='Nombre de la Facultad a la que pertenece')
    category = models.CharField(max_length=15, default='interno',
                                choices=[('interno', 'Interno'), ('externo', 'Externo')])
    center = models.CharField(max_length=150, default= INSTITUTION_FULL_NAME)

    def __str__(self):
        return self.user.get_full_name()

class PhdStudent(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    status= models.CharField(max_length=15, choices=[('solicitante', 'Solicitante'),('doctorando','Doctorando'), ('graduado', 'Graduado'), ('denegado', 'Denegado'), ('baja', 'Baja')])
    category= models.CharField(max_length=15,default='interno', choices=[('interno', 'Interno'),('externo','Externo')])
    center = models.CharField(max_length=150, default=INSTITUTION_FULL_NAME)

    def __str__(self):
        return self.student.user.username

class CursStudent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20,null=True, blank=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    request_date= models.DateField(default=now)
    graduate_date = models.DateField(null=True, blank=True)
    init_date = models.DateField(null=True, blank=True)
    country=models.CharField(max_length=70, default='Cuba')
    picture=models.ImageField(upload_to=student_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, default='f')
    birth_date=models.DateField(default=now)
    dni=models.CharField(max_length=24, default='12345678901')
    status = models.CharField(max_length=15,default='solicitante', choices=[('solicitante', 'Solicitante'), ('cursista', 'Cursista'),
                                                                            ('graduado', 'Graduado'), ('denegado', 'Denegado')])
    edition = models.ForeignKey(ProgramEdition, on_delete=models.CASCADE)
    category = models.CharField(max_length=15, default='interno',
                                choices=[('interno', 'Interno'), ('externo', 'Externo')])
    center = models.CharField(max_length=150, default= INSTITUTION_FULL_NAME)

    def __str__(self):
        return self.user.get_full_name()

class InnerAreas(models.Model):
    name = models.CharField(max_length=150, help_text='Areas administrativas para estudiantes internos')

    class Meta:
        verbose_name = 'Area administrativa interna'
        verbose_name_plural = 'Areas administrativas internas'

    def __str__(self):
        return self.name

# Modelo para verificar requisitos de ingreso al programa
class ProgramInitRequirements(models.Model):
    program= models.ForeignKey(Program, on_delete=models.CASCADE, help_text='Programa correspondiente')
    name = models.CharField(max_length=50, help_text='Nombre del requisito')
    description = models.CharField(max_length=150, help_text='Descripcion del requisito')

    class Meta:
        verbose_name='Requerimiento de inicio de programa'
        verbose_name_plural='Requerimientos de inicio de programa'

    def __str__(self):
        return self.name

class ProgramFinishRequirements(models.Model):
    program= models.ForeignKey(Program, on_delete=models.CASCADE, help_text='Programa correspondiente')
    name = models.CharField(max_length=50, help_text='Nombre del requisito')
    description = models.CharField(max_length=150, help_text='Descricpion del requisito')

    class Meta:
        verbose_name='Requerimiento de culminacion de programa'
        verbose_name_plural='Requerimientos de culminacion de programa'

    def __str__(self):
        return self.name

class StudentInitRequirement(models.Model):
    student= models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    msc_student= models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    curs_student = models.ForeignKey(CursStudent, null= True, on_delete=models.CASCADE)
    colecg_student = models.ForeignKey(ColegStudent, null=True, on_delete=models.CASCADE)
    requirement= models.ForeignKey(ProgramInitRequirements, on_delete=models.CASCADE)
    accomplished = models.BooleanField(default=False, help_text='Verdadero si esta satisfecho, Falso si lo contrario')

    def __str__(self):
        return 'Requirement'


class StudentFinishRequirement(models.Model):
    student = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    msc_student= models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    curs_student = models.ForeignKey(CursStudent, null= True, on_delete=models.CASCADE)
    colecg_student = models.ForeignKey(ColegStudent, null=True, on_delete=models.CASCADE)
    requirement = models.ForeignKey(ProgramFinishRequirements, on_delete=models.CASCADE)
    accomplished = models.BooleanField(default=False, help_text='Verdadero si esta satisfecho, Falso si lo contrario')

    def __str__(self):
        return 'Requirement'


class InvestigationProject(models.Model):
    program=models.ForeignKey(Program,null=True, on_delete=models.SET_NULL)
    line=models.ForeignKey(InvestigationLine,null=True, on_delete=models.SET_NULL)
    name=models.TextField(max_length=500)
    institution=models.CharField(max_length=120, help_text='Insitucion coordinadora')
    init_date =models.DateField(default=now, help_text='Fecha de inicio del proyecto')
    end_date =models.DateField(default=now, help_text='Fecha de fin del proyecto')

    def __str__(self):
        return self.name

class PhdStudentTheme(models.Model):
    phd_student=models.OneToOneField(PhdStudent, on_delete=models.CASCADE)
    project=models.ForeignKey(InvestigationProject, null=True, on_delete=models.SET_NULL)
    line=models.ForeignKey(InvestigationLine, null=True, on_delete=models.SET_NULL)
    description=models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.description


class PhdStudentThesis(models.Model):
    phd_student = models.OneToOneField(PhdStudent, on_delete=models.CASCADE)
    file = models.FileField(null=False, upload_to=phd_thesis_directory_path, help_text='Tesis')

    def __str__(self):
        return self.phd_student.phdstudenttheme.description

class PhdThesisComment(models.Model):
    thesis = models.ForeignKey(PhdStudentThesis, null=False, on_delete=models.CASCADE)
    date = models.DateField(auto_now=True)
    commenter_name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Nombre y apellidos", help_text="Nombre y apellidos del que comenta")
    commenter_email = models.EmailField(max_length=100, null=False, blank=False, verbose_name="Correo electrónico", help_text="Correo electrónico del que comenta")
    text = models.TextField(max_length=2000, null=False, blank=False, help_text="Comentario", verbose_name="Contenido del comentario")

    def __str__(self):
        return self.text

class PhdAnnouncement(models.Model):
    PRESENCIAL = "Presencial"
    ONLINE = "On-line"

    ANNOUNCEMENT_TYPE_CHOICES = [
        (PRESENCIAL , "Presencial"),
        (ONLINE , "On-line")
    ]

    phd_student = models.OneToOneField(PhdStudent, on_delete=models.CASCADE)
    date = models.DateTimeField(null=False, verbose_name="Fecha y hora de la defensa", help_text='Día y hora del acto de defensa de la tesis')
    thesis = models.OneToOneField(PhdStudentThesis, null=False, on_delete=models.CASCADE, help_text='Tesis lista para defensa')
    place = models.CharField(max_length=100, null=False, blank=False, verbose_name="Lugar", help_text="Lugar en que sesionará la defensa de la tesis" )
    url_vc = models.CharField(max_length=100, null=True, blank=True, verbose_name="URL de la sala", help_text="URL de la sala virtual de la videoconferencia" )
    type = models.CharField(max_length=20, choices=ANNOUNCEMENT_TYPE_CHOICES, default='Presencial', verbose_name="Modalidad", help_text="Modalidad: Presencial u Online")
    approval_resolution = models.CharField(max_length=10, verbose_name="Acuerdo de aprobación del tribunal", help_text="Número de acuerdo de la CNGC sobre aprobación del tribunal")
    sponsor = models.CharField(max_length=100, null=True, blank=True, default=settings.INSTITUTION_FULL_NAME, help_text="Instituciones que auspician el programa doctoral", verbose_name="Insituciones auspiciadoras")


    def __str__(self):
        return self.text


class PhdDefenseCourtMember(models.Model):
    MIEMBRO = "Miembro"
    SUPLENTE = "Suplente"

    ROLES_CHOICES = [
        (MIEMBRO, "Miembro"),
        (SUPLENTE, "Suplente")
    ]

    thesis = models.ForeignKey(PhdStudentThesis, null=False, on_delete=models.CASCADE, help_text='Tesis lista para defensa')
    name = models.CharField(max_length=30, null=False, blank=False, help_text="Nombre(s)")
    lastname = models.CharField(max_length=50, null=False, blank=False, help_text="Apellidos")
    center = models.CharField(max_length=60, null=False, blank=False, help_text="Centro de procedencia")
    role = models.CharField(max_length=20, choices=ROLES_CHOICES, verbose_name="Rol en el tribunal", help_text="Rol en el tribunal")

    def __str__(self):
        return "{0} {1}".format(self.name, self.lastname)



class MscStudentTheme(models.Model):
    student=models.OneToOneField(MscStudent, null= True, on_delete=models.CASCADE)
    project=models.ForeignKey(InvestigationProject, null=True, on_delete=models.SET_NULL)
    line=models.ForeignKey(InvestigationLine, null=True, on_delete=models.SET_NULL)
    description=models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.description

class CursStudentTheme(models.Model):
    student=models.OneToOneField(CursStudent, null= True, on_delete=models.CASCADE)
    project=models.ForeignKey(InvestigationProject, null=True, on_delete=models.SET_NULL)
    line=models.ForeignKey(InvestigationLine, null=True, on_delete=models.SET_NULL)
    description=models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.description
    
class ColegStudentTheme(models.Model):
    student=models.OneToOneField(ColegStudent, null= True, on_delete=models.CASCADE)
    project=models.ForeignKey(InvestigationProject, null=True, on_delete=models.SET_NULL)
    line=models.ForeignKey(InvestigationLine, null=True, on_delete=models.SET_NULL)
    description=models.TextField(max_length=500, null=True)

    def __str__(self):
        return self.description

class Tuthor(models.Model):
    phd_student=models.ForeignKey(PhdStudent, null=True,on_delete=models.CASCADE)
    msc_student=models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    curs_student=models.ForeignKey(CursStudent, null=True, blank=True, on_delete=models.CASCADE)
    coleg_student=models.ForeignKey(ColegStudent, null=True, blank=True, on_delete=models.CASCADE)
    
    professor = models.ForeignKey(ProgramMember, on_delete=models.CASCADE)

    def __str__(self):
        return self.professor.user.get_full_name()

class CGCBrief(models.Model):
    brief=models.FileField(upload_to=cgc_brief_path, null=True)
    year =models.IntegerField(default=now().year)
    month=models.CharField(max_length=12)
    update_date = models.DateField(default=now)

    def __str__(self):
        meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
                 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
        return 'Acta de la CGC-UNAH-Complejo de ' + meses[self.month] + ' de ' + str(self.year)


class CNGCBrief(models.Model):
    brief = models.FileField(upload_to=cngc_brief_path, null=True)
    year = models.IntegerField(default=now().year)
    month = models.CharField(max_length=12)
    update_date = models.DateField(default=now)


    def __str__(self):
        meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
                 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
        return 'Acta de la CNGC de ' + meses[self.month] +' de '+ str(self.year)

class ProgramBrief(models.Model):
    program=models.ForeignKey(Program, on_delete=models.CASCADE, null=True)
    brief = models.FileField(upload_to=program_brief_path)
    year = models.IntegerField(default=now().year)
    month = models.CharField(max_length=12)
    update_date = models.DateField(default=now)


    def __str__(self):
        meses = {1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio", 7: "Julio",
                 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"}
        return 'Acta de' + meses[self.month] +' de '+ str(self.year)

class Course(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    edition = models.ForeignKey(ProgramEdition,null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    description = models.TextField(max_length=500, null=True)
    init_date = models.DateField(default=now)
    end_date = models.DateField(null=True)

    def __str__(self):
        return self.name

class CourseProfessor(models.Model):
    professor = models.ForeignKey(ProgramMember, null=True,on_delete=models.SET_NULL)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)

    def __str__(self):
        if self.professor:
            return self.professor.user.get_full_name()
        return "Profesor no asignado"  # Mensaje alternativo



class CourseEvaluation(models.Model):
    phdstudent=models.ForeignKey(PhdStudent,null=True, on_delete=models.CASCADE)
    mscstudent=models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    dipstudent=models.ForeignKey(DipStudent, null=True, on_delete=models.CASCADE)
    colegstudent=models.ForeignKey(ColegStudent, null=True, on_delete=models.CASCADE)
    cursstudent=models.ForeignKey(CursStudent, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    value=models.SmallIntegerField()

    def __str__(self):
        return str(self.value)

class StudentFormationPlan(models.Model):
    phdstudent = models.OneToOneField(Student, on_delete=models.CASCADE)
    planned_end_year = models.IntegerField()
    elaboration_date = models.DateField(default=now)
    last_update_date = models.DateField(null=True)

    def __str__(self):
        return str(self.planned_end_year)


class FormationPlanActivities(models.Model):
    formation_plan = models.ForeignKey(StudentFormationPlan, on_delete=models.CASCADE)
    init_date = models.DateField(default=now)
    end_date = models.DateField()
    description = models.TextField(max_length=500)
    status = models.CharField(max_length=10, default='pending', choices=[['pending', 'Pendiente'], ['ready', 'Cumplida']])
    observations = models.TextField(max_length=200, null=True)

    def __str__(self):
        return self.description


class PostgMember(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    charge=models.CharField(max_length=20, choices=(('Director', 'Director'),('Metodólogo', 'Metodólogo'),('Técnico', 'Técnico')))
    grade = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    picture = models.ImageField(help_text='Foto', upload_to=postg_member_directory_path, null=True, blank=True)
    gender = models.CharField(max_length=1, default='f', choices=[('f', 'Femenino'), ('m', 'Masculino')])

    def __str__(self):
        return self.user.get_full_name()
    
class FormationMember(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    charge=models.CharField(max_length=20, choices=(('Director', 'Director'),('Metodólogo', 'Metodólogo'),('Técnico', 'Técnico')))
    grade = models.CharField(max_length=100,null=True, blank=True)
    phone = models.CharField(max_length=20,null=True, blank=True)
    picture = models.ImageField(help_text='Foto', upload_to=postg_member_directory_path, null=True, blank=True)
    gender = models.CharField(max_length=1, default='f', choices=[('f', 'Femenino'), ('m', 'Masculino')])

    def __str__(self):
        return self.user.get_full_name()

class Document(models.Model):
    name = models.CharField(max_length=100, null=False)
    year = models.IntegerField(null=False)
    month = models.CharField(max_length=12)
    description = models.TextField(max_length=300, null=True)
    type = models.CharField(max_length=20, null=False, default='acta',choices=[('acta', 'Acta'),('resolucion', 'Resolución'),('informe', 'Informe'),('otro', 'Otro')])
    doc = models.FileField(upload_to=postg_document_path)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class CGCDocument(models.Model):
    name = models.CharField(max_length=100, null=False)
    year = models.IntegerField(null=False)
    month = models.CharField(max_length=12)
    description = models.TextField(max_length=300, null=True)
    type = models.CharField(max_length=20, null=False, default='acta',choices=[('acta', 'Acta'),('resolucion', 'Resolución'),('informe', 'Informe'),('otro', 'Otro')])
    level = models.CharField(max_length=5, null=False, default='cgc',choices=[('cgc', 'Comisión de Grados Institucional'),('cngc', 'Comisión Nacional de Grados Científicos')])
    doc = models.FileField(upload_to=cgc_doc_path)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class ProgramDocument(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    year = models.IntegerField(null=False)
    month = models.CharField(max_length=12)
    description = models.TextField(max_length=300, null=True)
    type = models.CharField(max_length=20, null=False, default='acta',choices=[('acta', 'Acta'),('resolucion', 'Resolución'),('informe', 'Informe'),('otro', 'Otro')])
    doc = models.FileField(upload_to=program_document_path)
    is_public = models.BooleanField(default=False)

    def __str__(self):
        return self.description


# Modelo para gestionar expedientes de aspirantes
class ProgramFileDoc(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    doc_name = models.CharField(max_length=100, help_text='Nombre del documento', verbose_name='Nombre del documento')
    is_init_requirenment = models.BooleanField(default=False, help_text='Marcar si el documento es un requisito de ingreso', verbose_name='Es Requisito de ingreso')
    is_finish_requirenment = models.BooleanField(default=False, help_text='Marcar si el documento es un requisito de egreso', verbose_name='Es Requisito de egreso')
    just_for_nationals = models.BooleanField(default=False, help_text='Marcar si el documento es un requisito solo para aspirantes nacionales', verbose_name='Solo para nacionales')
    get_old = models.BooleanField(default=False, help_text='Marcar si el documento caduca', verbose_name='Caduca')
    type = models.CharField(max_length=20, null=False, default='student',
                            choices=[('student', 'Estudiante'), ('program', 'Programa'), ('comission', 'Comisión de grados')], verbose_name='Provisto por', help_text='Quién provee el documento')

    class Meta:
        verbose_name='Documento para el expediente de los estudiantes'
        verbose_name_plural='Documentos para el expediente de los estudiantes'

    def __str__(self):
        return self.doc_name

class StudentFileDocument(models.Model):
    student= models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    msc_student= models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    dip_student= models.ForeignKey(DipStudent, null=True, on_delete=models.CASCADE)
    coleg_student= models.ForeignKey(ColegStudent, null=True, on_delete=models.CASCADE)
    curs_student= models.ForeignKey(CursStudent, null=True, on_delete=models.CASCADE)
    program_file_document= models.ForeignKey(ProgramFileDoc, on_delete=models.CASCADE)
    accomplished = models.BooleanField(default=False, help_text='Verdadero si esta satisfecho, Falso si lo contrario')
    caducity_date = models.DateField(null=True, blank=True)
    file = models.FileField(upload_to=student_filedoc_directory_path, null=True)

    def __str__(self):
        return self.program_file_document.doc_name

class Message(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    program_receiver = models.ForeignKey(ProgramMember, null=True, on_delete=models.SET_NULL)
    phd_student_receiver = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    msc_student_receiver = models.ForeignKey(MscStudent, null=True, on_delete=models.SET_NULL)
    dip_student_receiver = models.ForeignKey(DipStudent, null=True, on_delete=models.SET_NULL)
    coleg_student_receiver = models.ForeignKey(ColegStudent, null=True, on_delete=models.SET_NULL)
    curs_student_receiver = models.ForeignKey(CursStudent, null=True, on_delete=models.SET_NULL)
    date = models.DateField(default=now)
    subject = models.CharField(max_length=250)
    body = models.TextField(max_length=4000)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class MessageSended(models.Model):
    sender = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    program_receiver = models.ForeignKey(ProgramMember, null=True, on_delete=models.SET_NULL)
    phd_student_receiver = models.ForeignKey(Student, null=True, on_delete=models.SET_NULL)
    msc_student_receiver = models.ForeignKey(MscStudent, null=True, on_delete=models.SET_NULL)
    dip_student_receiver = models.ForeignKey(DipStudent, null=True, on_delete=models.SET_NULL)
    coleg_student_receiver = models.ForeignKey(ColegStudent, null=True, on_delete=models.SET_NULL)
    curs_student_receiver = models.ForeignKey(CursStudent, null=True, on_delete=models.SET_NULL)
    context = models.CharField(max_length=12, null=False, default='personal',choices=[('students', 'Estudiantes'),('profesores', 'Profesores'),('comite', 'Comité'), ('personal', 'Personal')])
    date = models.DateField(default=now)
    subject = models.CharField(max_length=250)
    body = models.TextField(max_length=4000)
    readed = models.BooleanField(default=False)

    def __str__(self):
        return self.subject

class New(models.Model):
    program= models.ForeignKey(Program, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    body = models.TextField(max_length=5000, null=False)
    date = models.DateField(default=now)

    class Meta():
        verbose_name = 'Noticia de programa'
        verbose_name_plural = 'Noticias de programas'

    def __str__(self):
        return self.title

class Requester(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=False)
    last_name = models.CharField(max_length=100, null=False)
    email = models.EmailField(null=False)
    gender = models.CharField(max_length=1, null=False)
    dni = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=30, null=False)
    birthdate = models.DateField(null=False)
    theme = models.TextField(max_length=200, null=False)
    request_id = models.CharField(max_length=50, unique=True)
    request_date = models.DateTimeField(default=now)
    planned_end_year = models.IntegerField(null=False)
    line = models.IntegerField(null=False)

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class FAQ(models.Model):
    program = models.ForeignKey(Program, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255, verbose_name="Título")
    content = models.TextField(verbose_name="Contenido")
    date = models.DateField(default=now)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "Pregunta frecuente"
        verbose_name_plural = "Preguntas frecuentes"