from django.shortcuts import get_object_or_404, render,redirect
from .forms import ElevageForm,ActionForm
from .models import Elevage,Regle,Individu
from django.views.generic import ListView

def initial_elevage(request):
    if request.method=='GET':
        form=ElevageForm()
    elif request.method=='POST':
        form=ElevageForm(request.POST)
        if form.is_valid():
            elevage=form.save()
            for _ in range(elevage.males):
                 Individu.objects.create(
                    elevage=elevage,
                    sexe='M',
                    age_mois=3,
                    statut='P'
                )
            for _ in range(elevage.femelles):
                Individu.objects.create(
                    elevage=elevage,
                    sexe='F',
                    age_mois=3,
                    statut='P'
                )
            return redirect('elevage_app:FarmList')
    else:
        form=ElevageForm()
    return render(request,
                  'elevage_app/initial_elevage.html',{'form':form})
        
        
class FarmList(ListView):
    model = Elevage
    template_name = 'elevage_app/Farm_list.html'
    context_object_name = 'list_farm'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        search_query = self.request.GET.get('q')
        if search_query:
            queryset = queryset.filter(farm_nom__icontains=search_query)
        return queryset.order_by('farm_nom')
    
def EleVage(request,id:int):
    elevage=get_object_or_404(Elevage,pk=id)
    individus=elevage.individus.all()
    regles=Regle.objects.first()
    individus_presents = elevage.individus.filter(statut='P').count()
    capacite = elevage.calculer_capacite()
    place_disponible = capacite - individus_presents
    if request.method=='GET':
        form=ActionForm()
    elif request.method=='POST':
        form=ActionForm(request.POST)
        if form.is_valid():
            lapin_vendre = form.cleaned_data['lapin_vendre']
            acheter_nourriture = form.cleaned_data['acheter_nourriture']
            acheter_cages = form.cleaned_data['acheter_cages']
            
            # Validation des actions
            errors = []
            
            if lapin_vendre > elevage.a_vendre:
                errors.append("Nombre de lapins à vendre invalide")
            
            cout_total = (float(acheter_nourriture )* float(regles.prix_nourriture) + 
                         float(acheter_cages) * float(regles.prix_cage))
            
            if cout_total > elevage.argent:
                errors.append("Fonds insuffisants pour ces achats")
            
            if not errors:
                elevage.jouer_tour(lapin_vendre, acheter_nourriture, acheter_cages)
                return redirect('elevage_app:EleVage', id=id)
            else:
                return render(request, 'elevage_app/elevage.html', {
                    'elevage': elevage,
                    'individus': individus,
                    'form': form,
                    'errors': errors
                })
    else:
        form = ActionForm(initial={
            'lapin_vendre': 0,
            'acheter_nourriture': 0,
            'acheter_cages': 0
        })
    
    return render(request, 'elevage_app/elevage.html', {
        'elevage': elevage,
        'individus': individus,
        'form': form,
        'individus_presents': individus_presents,
        'capacite': capacite,
        'place_disponible': place_disponible,
        'regles': regles
    })
    
        
    
    

# Create your views here.
