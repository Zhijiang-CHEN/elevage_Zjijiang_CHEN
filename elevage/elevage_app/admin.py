from django.contrib import admin
from .models import Elevage
from elevage_app.models import Elevage,Individu,Regle

admin.site.register(Elevage)
admin.site.register(Individu)
admin.site.register(Regle)
# Register your models here.
