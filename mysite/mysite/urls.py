
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
    path('status/', views.status, name='status'),
    path('garage/',views.garage, name='garage'),
    path('', include('photos.urls')),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

