from django.urls import path

from . import views

app_name='elevage_app'
urlpatterns = [
    path("FarmList/",views.FarmList,name="FarmList"),
    path("initial_elevage/",views.initial_elevage,name='initial_elevage'),
  
]