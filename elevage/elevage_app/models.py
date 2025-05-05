from decimal import Decimal
import random
from django.db import models
from django.urls import reverse
from django.db.models import F

class Elevage(models.Model):
    farm_nom = models.CharField(max_length=100,unique=True)  #nom de la farm
    males = models.PositiveIntegerField(default=0)
    femelles = models.PositiveIntegerField(default=0)
    reproducteurs = models.PositiveIntegerField(default=0)
    a_vendre = models.PositiveIntegerField(default=0)
    nourriture_kg = models.FloatField(default=0)
    cages = models.PositiveIntegerField(default=1)
    argent = models.DecimalField(max_digits=10, decimal_places=2, default=1000)
    mois_ecoules = models.PositiveIntegerField(default=0)
    def get_absolute_url(self):
        return reverse('elevage_app:EleVage', kwargs={'id': self.id})
    
    def calculer_capacite(self):
        regle, created = Regle.objects.get_or_create(
        defaults={
            'prix_nourriture': 1.0,
            'prix_cage': 50.0,
            'prix_vente_lapin': 20.0,
            'consommation_1mois': 0.1,
            'consommation_2mois': 0.25,
            'consommation_3mois': 0.25,
            'portee_max': 4,
            'cage_max': 6,
            'cage_surcharge': 10,
            'age_min_gravidite_mois': 6,
            'age_max_gravidite_mois': 48,
            'duree_gestation_mois': 1
        }
    )
        return self.cages * regle.cage_max
    
    def calculer_place_disponible(self):
        return self.calculer_capacite() - self.individus.filter(statut='P').count()
    
    def jouer_tour(self,Lapin_vendre,acheter_nourriture,acheter_cages):
        regle=Regle.objects.first()
        
        #vendre les lapins
        self.a_vendre-=Lapin_vendre
        a_vendu=Individu.objects.filter(statut='P',elevage=self,age_mois__gte=3).order_by('?')[:Lapin_vendre]
        for lapins in a_vendu:
            lapins.statut='V'
        self.argent+=Lapin_vendre*regle.prix_vente_lapin
        
        #acheter les ressource
        self.argent-=Decimal(str(acheter_nourriture))*regle.prix_nourriture
        self.nourriture_kg+=acheter_nourriture
        self.argent-=acheter_cages*regle.prix_cage
        self.cages+=acheter_cages
        
        #Augumenter l'age des lapins
        # 获取要更新的主键列表
        #ids_to_update = Individu.objects.filter(elevage=self).values_list('id', flat=True)[:10]

        # 然后更新这些记录
        #Individu.objects.filter(id__in=ids_to_update).update(age_mois=F('age_mois') + 1)
        for individu in Individu.objects.filter(elevage=self):
            individu.age_mois += 1
            individu.save()
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
                    genders=['F','M']
                    sexe=random.choice(genders)
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
    enceinte = models.BooleanField(default=False)
    mois_gestation = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.age_mois}mois-{self.get_sexe_display()}-{self.get_statut_display()}"
    
class Regle(models.Model):
    prix_nourriture = models.DecimalField(max_digits=6, decimal_places=2,default=10)
    prix_cage = models.DecimalField(max_digits=6, decimal_places=2,default=10)
    prix_vente_lapin = models.DecimalField(max_digits=6, decimal_places=2,default=10)
    consommation_1mois = models.FloatField(max_length=2,default=0.0)
    consommation_2mois = models.FloatField(max_length=2,default=3.1)
    consommation_3mois = models.FloatField(max_length=2,default=7.5)
    portee_max = models.PositiveIntegerField(default=4,verbose_name="Maximam de nombre de chaque femelle")
    cage_max = models.PositiveIntegerField(default=6,verbose_name="nombre adoptee")
    cage_surcharge=models.PositiveIntegerField(default=10,verbose_name="Maximam de lapins dans chaque cage")
    age_min_gravidite_mois = models.PositiveIntegerField(default=3,verbose_name="Minimum age")
    age_max_gravidite_mois = models.PositiveIntegerField(default=48,verbose_name="maximam age")
    duree_gestation_mois = models.PositiveBigIntegerField(default=1,verbose_name="duree_gestion")
    def __str__(self):
        return "Regles du jeu"
    class Meta:
        verbose_name = "Règle"
        verbose_name_plural = "Règles"
        
    
    
    
    
    
# Create your models here.
