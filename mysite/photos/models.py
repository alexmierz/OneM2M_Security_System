from django.db import models
from django import forms


class Photo(models.Model): 
    Title = models.CharField(max_length=50)
    File = models.FileField()
    



#class Photo(models.Model):
   # class Meta:
#        model = forms
#        fields = ['title', 'file']

