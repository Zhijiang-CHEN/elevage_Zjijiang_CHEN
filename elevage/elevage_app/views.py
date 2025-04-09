from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ElevageForm

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def initial_elevage(request):
    if request.method=='GET':
        form=ElevageForm()
    elif request.method=='POST':
        form=ElevageForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('elevage:list')
    return render(request,
                  'elevage_app/initial_elevage.html',{'form':form})
        
        
    
    

# Create your views here.
