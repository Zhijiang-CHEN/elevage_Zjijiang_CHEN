from django import forms
from .models import Elevage
class ElevageForm(forms.ModelForm):
    class Meta:
        model=Elevage
        fields='__all__'
        widgets = {
            'farm_nom': forms.TextInput(attrs={'class': 'form-control'}),
            'males': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'femelles': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'nourriture_kg': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
            'cages': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'argent': forms.NumberInput(attrs={'class': 'form-control', 'min': 0}),
        }
        labels = {
            'farm_nom': 'Nom de la ferme',
            'males': 'Nombre de mâles initiaux',
            'femelles': 'Nombre de femelles initiales',
            'nourriture_kg': 'Nourriture initiale (kg)',
            'cages': 'Nombre de cages initiales',
            'argent': 'Argent initial',
        }
        
        
class ActionForm(forms.Form):
    males_vendre=forms.IntegerField(min_value=0,label="males a vendre")
    femelles_vendre=forms.IntegerField(min_value=0,label="femelle a vendre")
    lapin_vendre=forms.IntegerField(min_value=0,
        label="Lapins à vendre",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de lapins à vendre'}
        ))
    
    acheter_nourriture=forms.FloatField(min_value=0,
        label="Nourriture à acheter (kg)",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantité de nourriture'
        }))
    acheter_cages=forms.IntegerField(  min_value=0,
        label="Cages à acheter",
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nombre de cages'
        }))
    
    
    