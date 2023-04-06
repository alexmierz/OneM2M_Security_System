
from django import views


from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf import settings #file upload
from django.conf.urls.static import static #file upload

from . import views



urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', views.home, name='home'),

    path('status/', views.create, name='status'),
    path('upload/', views.upload, name='upload'),
    path('garage/',views.garage, name='garage'),
    #path('garage/',views.garage),
    #path('status', views.status),
    #path('status.html', views.status, name="status"),
    #path('', include ('main.urls')),
] 

