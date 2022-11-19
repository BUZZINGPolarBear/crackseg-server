from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns = [
    path('test/', views.testResponse),
    path('fileupload/', fileUpload, name="fileupload"),
    path('fileuplaod/detailed', detailInference, name="detailInference"),
    path('vision-inference/', visionInference, name="computerVisionInference"),
    path('vision-inference/info/', visionInferenceInfo, name="visionInfernceInfo"),
    path('remove-imgs/', removeImgs, name="remove-images"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)