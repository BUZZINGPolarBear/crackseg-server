from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns = [
    path('test/', views.testResponse),
    path('fileupload/', fileUpload, name="fileupload"),
    path('fileuplaod/detailed', detailInference, name="detailInference"),
    path('run/detailed', runDetailInference, name="runDatailInference"),
    path('vision-inference/', visionInference, name="computerVisionInference"),
    path('vision-inference/info/', visionInferenceInfo, name="visionInfernceInfo"),
    path('remove-imgs/', removeImgs, name="remove-images"),
    path('remove-imgs/detailed', removeUnusefulImgs, name="remove-unuseful images"),

    path('app/run/detailed', runMQDetailInference),
    path('app/run/detailed/test', testrunMQDetailInference),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)