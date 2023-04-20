from django import forms
from photos.models import Photo


class PhotoUpload(forms.ModelForm):

    class Meta:
        model = Photo
        fields = ('Title', 'File')

        widgets = {
            'Title': forms.TextInput(attrs={}),
            'File': forms.FileInput(attrs={}),
            

        }