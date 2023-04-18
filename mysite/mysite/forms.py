from django import forms
#from .models import Photo

class PhotoForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()