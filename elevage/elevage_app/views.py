from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from .forms import ElevageForm
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
    individus=elevage.individus.all()
    return render(request,'elevage_app/elevage.html',{'elevage':elevage,'Individus':individus})
    

    
        
    
    

# Create your views here.
