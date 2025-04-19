from django import forms
from .models import Elevage
class ElevageForm(forms.ModelForm):
    class Meta:
        model=Elevage
        fields='__all__'
        
        
class ActionForm(forms.Form):
    vendre=forms.IntegerField(min_value=0,label="Lapins a vendre")
    acheter_nourriture=forms.FloatField(min_value=0,label="Nourriture a acheter_kg")
    acheter_cages=forms.IntegerField(min_value=0,label="Cages a acheter")
    
    
    