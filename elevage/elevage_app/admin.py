from django.contrib import admin
from .models import Elevage
from elevage_app.models import Elevage,Individu

admin.site.register(Elevage)
admin.site.register(Individu)
# Register your models here.
