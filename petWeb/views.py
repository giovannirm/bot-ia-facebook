from django.shortcuts import render, redirect
from .models import Diseases
from django.views.decorators.csrf import csrf_exempt

def home(request):
    return render(request,'home.html')

def login(request):    
    if request.method =='POST':                
        user = request.POST['user']
        password = request.POST['password']
        if user == 'admin' and password == 'admin':
            return redirect('home')
        else:
            return redirect('login')
    return render(request,'login.html')

@csrf_exempt
def add_disease(request):    
    if request.method == 'POST':
        symptom = request.POST.get('symptom').split(', ')
        disease = Diseases(name = request.POST.get('name'), symptom = symptom, race = request.POST.get('race'), answer = request.POST.get('answer'))
        disease.save()
        return redirect('read')        
    return render(request,'add_disease.html')

def update_disease(request, id):
    pass

def delete_disease(request, id):
    pass

def read_diseases(request):
    
    return render(request,'diseases.html')