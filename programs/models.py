from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import now

def program_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/imgs/{1}'.format(instance.slug, filename)

def member_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/members/{1}/{2}'.format(instance.program.slug,instance.id, filename)

def student_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/students/{1}/{2}'.format(instance.program.slug,instance.id, filename)

def background_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/imgs/backgrounds/{1}'.format(instance.program.slug, filename)

def cgc_photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cgc/imgs/<filename>
    return 'cgc/imgs/{0}'.format(filename)

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
    type=models.CharField(max_length=20,choices=[('phd','Doctorado'),('msc','Maestría'),('dip','Diplomado')], verbose_name='Tipo')
    slug=models.SlugField(max_length=40,help_text='Slug para url',unique=True)
    address = models.TextField(max_length=150, help_text='Dirección de la sede del programa')
    phone = models.CharField(max_length=20, help_text='Teléfono de contacto')
    email = models.EmailField(help_text='Email de contacto')
    icon = models.CharField(max_length=100, null=False, blank=False, choices=ICON_CHOICES,
                            help_text='Seleccione una opcion de la lista')
    background = models.ImageField(upload_to=program_directory_path, blank=True)

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
    name=models.CharField(max_length=50, help_text='Nombre', verbose_name='Nombre')
    lastname=models.CharField(max_length=70, help_text='Apellidos', verbose_name='Apellidos')
    charge = models.CharField(max_length=50,choices=[('Presidente','Presidente'),('Secretario','Secretario'),('Miembro','Miembro')], help_text='Cargo', verbose_name='Cargo')
    priority= models.SmallIntegerField(help_text="Prioridad del Cargo", choices=[(1,'1'),(2,'2'),(3,'3')])
    fb_contact = models.URLField(help_text='URL del contacto de Facebook',default='https://www.facebook.com',  blank=True)
    tw_contact = models.URLField(help_text='URL del contacto de Twitter',default='https://www.twitter.com',  blank=True)
    in_contact = models.URLField(help_text='URL del contacto de Linkedin',default='https://www.linkedin.com',  blank=True)
    gp_contact = models.URLField(help_text='URL del contacto de Google+',default='https://plus.google.com', blank=True)
    picture= models.ImageField(help_text='Foto', upload_to=cgc_photo_directory_path, null=True, blank=True)
    gender=models.CharField(max_length=1, choices=[('f','Femenino'),('m','Masculino')], help_text='Género')

    class Meta:
        verbose_name = 'Miembro de la CGC'
        verbose_name_plural = 'Miembros de la CGC'

    def __str__(self):
        return self.name

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
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    country = models.CharField(max_length=70, default='Cuba')
    phone = models.CharField(max_length=50)
    institution = models.CharField(max_length=100)
    birth_date = models.DateField(default='1960-01-01', help_text='Fecha de nacimiento')
    degree = models.CharField(max_length=100,
                                   help_text='Grado cientifico')
    picture = models.ImageField(null=True, upload_to=member_directory_path)
    fb_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Facebook del miembro del tribunal')
    tw_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Twitter del miembro del tribunal')
    ln_contact = models.CharField(max_length=50, null=True, blank=True,
                                  help_text='Contacto de Linkedin del miembro del tribunal')
    init_date = models.DateField(default=now)
    sex = models.CharField(max_length=2, choices=SEX_CHOICES, help_text='Sexo del miembro del tribunal')
    weight=models.SmallIntegerField(help_text="Peso del Cargo", choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')])

    class Meta:
        verbose_name='Miembro del Programa'
        verbose_name_plural='Miembros del programa'

    def __str__(self):
        return self.user.get_full_name()

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
    dni=models.CharField(max_length=11, default='12345678901')

    def __str__(self):
        return self.user.get_full_name()

class MscStudent(models.Model):
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
    dni=models.CharField(max_length=11, default='12345678901')
    status = models.CharField(max_length=15, choices=[('solicitante', 'Solicitante'), ('maestrante', 'Maestrante'),
                                                      ('graduado', 'Graduado')])

    def __str__(self):
        return self.user.get_full_name()

class PhdStudent(models.Model):
    student = models.OneToOneField(Student,on_delete=models.CASCADE)
    status= models.CharField(max_length=15, choices=[('solicitante', 'Solicitante'),('doctorando','Doctorando'), ('graduado', 'Graduado')])

    def __str__(self):
        return self.student.user.username

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
    requirement= models.ForeignKey(ProgramInitRequirements, on_delete=models.CASCADE)
    accomplished = models.BooleanField(default=False, help_text='Verdadero si esta satisfecho, Falso si lo contrario')

    def __str__(self):
        return 'Requirement'


class StudentFinishRequirement(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    msc_student= models.ForeignKey(MscStudent, null=True, on_delete=models.CASCADE)
    requirement = models.ForeignKey(ProgramFinishRequirements, on_delete=models.CASCADE)
    accomplished = models.BooleanField(default=False, help_text='Verdadero si esta satisfecho, Falso si lo contrario')

    def __str__(self):
        return 'Requirement'

class InvestigationLine(models.Model):
    program=models.ForeignKey(Program, on_delete=models.CASCADE)
    name=models.TextField(max_length=500, help_text='Nombre de la linea')

    def __str__(self):
        return self.name

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


