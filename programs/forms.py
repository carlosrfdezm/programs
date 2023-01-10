from django import forms

from programs.models import PhdAnnouncement


class FileUploadForm(forms.Form):
    file_source = forms.FileField()



class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = PhdAnnouncement
        fields = '__all__'
