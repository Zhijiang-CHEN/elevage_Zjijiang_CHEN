import random
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
    def jouer_tour(self,Lapin_vendre,acheter_nourriture,acheter_cages):
        regle=Regle.objects.first()
        
        #vendre les lapins
        self.a_vendre-=Lapin_vendre
        a_vendu=Individu.objects.filter(statut='P',elevage=self,age_mois__gte=3).order_by('?')[:Lapin_vendre]
        for lapins in a_vendu:
            lapins.statut='V'
        self.argent+=Lapin_vendre*regle.prix_vente_lapin
        
        #acheter les ressource
        self.argent-=acheter_nourriture*regle.prix_nourriture
        self.nourriture_kg+=acheter_nourriture
        self.argent-=acheter_cages*regle.prix_cage
        self.cages+=acheter_cages
        
        #Augumenter l'age des lapins
        Individu.objects.filter(elevage=self).update(age_mois=Individu.age_mois+1)
        
        #logique pour reproducteur
        femelle_reproductrices=Individu.objects.filter(
            elevage=self,
            sexe='F',
            age_mois__gte=6,
            age_mois__lte=48,
            statut='P'
        )
        for femelle in femelle_reproductrices:
            if random.random()<0.8:
                portee=random.randint(1,regle.portee_max)
                for _ in range(portee):
                    sexe=random.choice['M','F']
                    Individu.objects.create(
                        elevage=self,
                        sexe=sexe,
                        age_mois=0,
                        statut='P'
                    )
            femelle.statut='G'
        #Calculer la consommation de nourriture
        total_nourriture=0
        for lapins in Individu.objects.filter(elevage=self,statut='P'):
            if lapins.age_mois==0:
                continue
            elif 1<=lapins.age_mois<3:
                total_nourriture+=0.1
            else:
                total_nourriture+=0.25
        self.nourriture_kg-=total_nourriture*30
        
        #Calculer si il y a mort pour les nourriture insuiffisant
        if self.nourriture_kg<0:
            morts=Individu.objects.filter(elevage=self,statut='P').order_by('?')[:abs(int(self.nourriture_kg/0.25))]
            morts.update(statut='M')
            self.nourriture_kg=0
            
        #Dans la situation de la cage
        Cage_adopte=6
        lapins_vivants=Individu.objects.filter(elevage=self,statut='P').count()
        capacite_total=self.cages*regle.cage_max
        if lapins_vivants>capacite_total:
            surplus=(lapins_vivants-capacite_total)
            lapins_adultes=Individu.objects.filter(
                elevage=self,
                statut='P',
                age_mois__gte=1
            ).order_by('?')[:surplus]
            lapins_adultes.update(statut='M')
            
        #Nouveaux le statut du jeu 
        self.mois_ecoules+=1
        self.save()
        
     
        
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
    consommation_1mois = models.FloatField(max_length=20)
    consommation_2mois = models.FloatField(max_length=20)
    consommation_3mois = models.FloatField(max_length=20)
    portee_max = models.PositiveIntegerField(default=4,verbose_name="Maximam de nombre de chaque femelle")
    cage_max = models.PositiveIntegerField(default=6,verbose_name="nombre adoptee")
    cage_surcharge=models.PositiveIntegerField(default=10,verbose_name="Maximam de lapins dans chaque cage")
    age_min_gravidite_mois = models.PositiveIntegerField(default=6,verbose_name="Minimum age")
    age_max_gravidite_mois = models.PositiveIntegerField(default=48,verbose_name="maximam age")
    duree_gestation_mois = models.PositiveBigIntegerField(default=1,verbose_name="duree_gestion")
    def __str__(self):
        return "Regles du jeu"
    
    
    
    
    
# Create your models here.
