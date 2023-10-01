from django import forms
from .models import Photo,Info_img

class UploadModelForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
class Upload_infoimg_Form(forms.ModelForm):
    class Meta:
        model = Info_img
        fields = ('image',)
        widgets = {
            'image': forms.FileInput(attrs={'class': 'form-control-file'})
        }
