from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views
from .views import *

urlpatterns = [
    path('', views.indexPage, name="home"),
    path('loading/', views.loadingPage, name="loadingPage"),
    path('result/', views.resultPage, name="segmantationResult"),
    path('result/detailed', views.detailedResultPage, name="detailedSegmantationResult")
]