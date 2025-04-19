from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from .forms import ElevageForm,ActionForm
from .models import Elevage

def initial_elevage(request):
    if request.method=='GET':
        form=ElevageForm()
    elif request.method=='POST':
        form=ElevageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('elevage_app:initial_elevage')
    return render(request,
                  'elevage_app/initial_elevage.html',{'form':form})
        
        
def FarmList(request):
    list_farm=Elevage.objects.order_by("farm_nom")
    context={"list_farm":list_farm}
    return render(request,"elevage_app/Farm_list.html",context)

def EleVage(request,id:int):
    elevage=get_object_or_404(Elevage,pk=id)
    if request.method=='GET':
        form=ActionForm()
    elif request.method=='POST':
        form=ActionForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['vendre'] > Elevage.a_vendre:
                return render(request,'elevage_app/elevage.html',{'error':'Nombre de lapins a vendre invalide'})  
            # ne pas oublier ajouter le contraints de ressource
            else:
                elevage.a_vendre-=form.cleaned_data['vendre']
                elevage.cages+=form.cleaned_data['acheter_cages']
                elevage.nourriture_kg+=form.cleaned_data['acheter_nourriture']
                #ne pas oublier ajouter le cahnge d'argent
                form.save()
                return redirect('EleVage',pk=id)
        else:
            form=ActionForm()      
            individus=elevage.individus.all()
            return render(request,'elevage_app/elevage.html',{'elevage':elevage,'Individus':individus})
    

    
        
    
    

# Create your views here.
