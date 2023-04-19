from django.db import models
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class Author(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title
    

class Post(models.Model):
    title = models.CharField(max_length=50)
    overview = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    comment_count = models.IntegerField(default=0)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    thumbnail = models.ImageField()
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return self.title
    
    

class Photo(models.Model): 
    Title = models.CharField(max_length=50)
    File = models.FileField(null=True, blank=True, upload_to="images/")
    



#class Photo(models.Model):
   # class Meta:
#        model = forms
#        fields = ['title', 'file']

