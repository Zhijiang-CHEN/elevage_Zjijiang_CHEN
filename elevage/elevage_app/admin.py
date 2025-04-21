from django.contrib import admin
from .models import Elevage
from elevage_app.models import Elevage,Individu,Regle

admin.site.register(Elevage)
class ElevageAdmin(admin.ModelAdmin):
    list_display = ('farm_nom', 'males', 'femelles', 'a_vendre', 'nourriture_kg', 'cages', 'argent', 'mois_ecoules')
    list_filter = ('mois_ecoules',)
    search_fields = ('farm_nom',)
    readonly_fields = ('mois_ecoules',)
admin.site.register(Individu)
class IndividuAdmin(admin.ModelAdmin):
    list_display = ('elevage', 'get_sexe_display', 'age_mois', 'get_statut_display')
    list_filter = ('elevage', 'sexe', 'statut')
    search_fields = ('elevage__farm_nom',)
admin.site.register(Regle)
class RegleAdmin(admin.ModelAdmin):
    list_display = ('prix_nourriture', 'prix_cage', 'prix_vente_lapin', 'portee_max', 'cage_max')
    
    def has_add_permission(self, request):
        return not Regle.objects.exists()
# Register your models here.
