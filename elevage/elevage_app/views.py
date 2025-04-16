from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ElevageForm

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
        
        
    
    

# Create your views here.
