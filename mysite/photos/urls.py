from django.urls import path
from . import views
from .views import face_recognition
import face_recognition
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('upload/', views.photo_upload_view, name='upload') 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

