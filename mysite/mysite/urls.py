
from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf import settings #file upload
from django.conf.urls.static import static #file upload





urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    #path('', include ('main.urls')),
] 

