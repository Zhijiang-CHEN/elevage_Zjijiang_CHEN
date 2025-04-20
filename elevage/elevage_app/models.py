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
    
class  Individu(models.Model):
    SEXE_CHOICES=[('M','Male'),('F','Femelle')]
    STATUT_CHOICES=[
        ('P','Present'),
        ('V','Vendu'),
        ('M','Mort'),
        ('G','Gravide')
        
    ]
    elevage=models.ForeignKey(Elevage,on_delete=models.CASCADE,related_name='individus')
    sexe=models.CharField(max_length=1,choices=SEXE_CHOICES)
    age_mois=models.PositiveIntegerField(default=0)
    statut=models.CharField(max_length=1,choices=STATUT_CHOICES)
    def __str__(self):
        return f"{self.age_mois}-{self.sexe}-{self.statut}"
    
class Regle(models.Model):
    prix_nourriture = models.DecimalField(max_digits=6, decimal_places=2)
    prix_cage = models.DecimalField(max_digits=6, decimal_places=2)
    prix_vente_lapin = models.DecimalField(max_digits=6, decimal_places=2)
    consommation_1mois = models.FloatField()
    consommation_2mois = models.FloatField()
    consommation_3mois = models.FloatField()
    portee_max = 4
    cage_max = models.PositiveIntegerField()
    age_min_gravidite_mois = 6
    age_max_gravidite_mois = 54
    duree_gestation_mois = 1
    def __str__(self):
        return "Regles du jeu"
    
    
    
    
    
# Create your models here.
