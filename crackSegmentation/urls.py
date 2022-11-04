from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns = [
    path('test/', views.testResponse),
    path('fileupload/', fileUpload, name="fileupload"),
    path('prediction-end/', predictionEnd, name="prediction-end")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)