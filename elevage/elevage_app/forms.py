from django import forms
from .models import Elevage
class ElevageForm(forms.ModelForm):
    class Meta:
        model=Elevage
        fields='__all__'
        
        
class ActionForm(forms.Form):
    males_vendre=forms.IntegerField(min_value=0,label="males a vendre")
    femelles_vendre=forms.IntegerField(min_value=0,label="femelle a vendre")
    lapin_vendre=forms.IntegerField(min_value=0,label="lapins a vendre")
    acheter_nourriture=forms.FloatField(min_value=0,label="Nourriture a acheter_kg")
    acheter_cages=forms.IntegerField(min_value=0,label="Cages a acheter")
    
    
    