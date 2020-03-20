from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinLengthValidator
from django.utils.timezone import now

def program_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/imgs/program_<slug>/<filename>
    return 'program_{0}/imgs/{1}'.format(instance.slug, filename)

def cgc_photo_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/cgc/imgs/<filename>
    return 'cgc/imgs/{0}'.format(filename)

# Create your models here.

ion_ios_alarm_outline = 'ion-ios-alarm-outline'
ion_ios_albums_outline = 'ion-ios-albums-outline'
ion_ios_barcode_outline = 'ion-ios-barcode-outline'
ion_ios_body_outline = 'ion-ios-body-outline'
ion_ios_book_outline = 'ion-ios-book-outline'
ion_ios_calculator_outline = 'ion-ios-calculator-outline'
ion_ios_cloudy_outline = 'ion-ios-cloudy-outline'
ion_ios_medical_outline = 'ion-ios-medical-outline'

ICON_CHOICES = (
    (ion_ios_alarm_outline, 'ion-ios-alarm-outline'),
    (ion_ios_albums_outline, 'ion-ios-albums-outline'),
    (ion_ios_barcode_outline, 'ion-ios-barcode-outline'),
    (ion_ios_body_outline, 'ion-ios-body-outline'),
    (ion_ios_book_outline, 'ion-ios-book-outline'),
    (ion_ios_calculator_outline, 'ion-ios-calculator-outline'),
    (ion_ios_cloudy_outline, 'ion-ios-cloudy-outline'),
    (ion_ios_medical_outline, 'ion-ios-medical-outline'),
)

class Program(models.Model):
    full_name=models.CharField(max_length=150, help_text='Nombre completo del programa', verbose_name='Nombre completo')
    short_name=models.CharField(max_length=40, help_text='Nombre corto del programa', verbose_name='Nombre Corto')
    description=models.TextField(max_length=200, help_text='Breve descripcion del programa', verbose_name='Descripcion')
    type=models.CharField(max_length=20,choices=[('phd','Doctorado'),('msc','Maestría')], verbose_name='Tipo')
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

class CGC_Member(models.Model):
    name=models.CharField(max_length=120, help_text='Nombre y apellidos', verbose_name='Nombre y apellidos')
    charge = models.CharField(max_length=50,choices=[('president','Presidente'),('secretary','Secretario'),('member','Miembro')], help_text='Cargo', verbose_name='Cargo')
    priority= models.SmallIntegerField(help_text="Prioridad del Cargo", choices=[(1,'1'),(2,'2'),(3,'3')])
    fb_contact = models.URLField(help_text='URL del contacto de Facebook')
    tw_contact = models.URLField(help_text='URL del contacto de Twitter')
    in_contact = models.URLField(help_text='URL del contacto de Linkedin')
    gp_contact = models.URLField(help_text='URL del contacto de Google+')
    picture= models.ImageField(help_text='Foto', upload_to=cgc_photo_directory_path)

    class Meta:
        verbose_name = 'Miembro de la CGC'
        verbose_name_plural = 'Miembros de la CGC'

    def __str__(self):
        return self.name

