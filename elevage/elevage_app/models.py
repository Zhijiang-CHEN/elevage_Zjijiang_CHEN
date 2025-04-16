from django.db import models

class Elevage(models.Model):
    farm_nom = models.CharField(max_length=100)  #nom de la farm
    males = models.PositiveIntegerField(default=0)
    femelles = models.PositiveIntegerField(default=0)
    reproducteurs = models.PositiveIntegerField(default=0)
    a_vendre = models.PositiveIntegerField(default=0)
    nourriture_kg = models.FloatField(default=0)
    cages = models.PositiveIntegerField(default=1)
    argent = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    mois_ecoules = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.farm_nom
    
    
    
# Create your models here.
