from django.urls import path

from . import views

app_name='elevage_app'
urlpatterns = [
     path('<int:id>/', views.EleVage, name='EleVage'),
    path("FarmList/",views.FarmList.as_view(),name="FarmList"),
    path("initial_elevage/",views.initial_elevage,name='initial_elevage'),
  
]