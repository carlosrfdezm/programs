from django import forms

from programs.models import PhdAnnouncement, PhdStudentThesis, PhdThesisComment


class FileUploadForm(forms.Form):
    file_source = forms.FileField()



class AnnouncementForm(forms.ModelForm):
    class Meta:
        model = PhdAnnouncement
        fields = '__all__'

class PhdStudentThesisForm(forms.ModelForm):

    class Meta:
        model = PhdStudentThesis
        fields = '__all__'


class PhdThesisCommentForm(forms.ModelForm):

    class Meta:
        model = PhdThesisComment
        fields = '__all__'

