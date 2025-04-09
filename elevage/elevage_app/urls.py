from django.urls import path

from . import views

urlpatterns = [
    path("",views.initial_elevage,name="initial_elevage"),
  
]