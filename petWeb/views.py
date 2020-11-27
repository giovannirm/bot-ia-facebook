from django.shortcuts import render, redirect
from .models import Diseases
from django.views.decorators.csrf import csrf_exempt
#from django.http import HttpResponse

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
        symptom = request.POST.get('symptom').lower().split(', ')        
        disease = Diseases(name = request.POST.get('name').lower(), symptom = symptom, race = request.POST.get('race').lower(), answer = request.POST.get('answer').lower())
        disease.save()
        return redirect('read')        
    return render(request,'add_disease.html')

@csrf_exempt
def update_disease(request):
    id = request.POST.get('id')
    disease = Diseases.objects.get(id = id)
    disease.race = request.POST.get('race')
    disease.name = request.POST.get('name') 
    disease.symptom = request.POST.get('symptom').lower().split(', ')
    disease.answer = request.POST.get('answer')
    disease.save()
    return redirect('read')
 
def delete_disease(request, id): 
    if request.method == 'GET':
        disease = Diseases.objects.get(id = id)
        disease.delete()
    return redirect('read')    

def read_diseases(request):
    diseases = Diseases.objects.all()
    context = {
        'diseases': diseases
    }
    return render(request,'diseases.html', context)

def modal_update(request, id):
    disease = Diseases.objects.get(id = id)
    cadena = ""
    i = 0
    for sym in disease.symptom:
        if i > 0:
            cadena = cadena + ", " + sym
        if i == 0:
            cadena = cadena + sym
        i = i + 1        

    if request.method =='GET':        
        context = {
            'id': disease.id,
            'symptom': cadena,
            'race': disease.race,
            'name': disease.name,
            'answer': disease.answer
        }      
    return render(request,'modal_update.html', context)

def modal_read(request, id):
    disease = Diseases.objects.get(id = id)
    cadena = ""
    i = 0
    for sym in disease.symptom:
        if i > 0:
            cadena = cadena + ", " + sym
        if i == 0:
            cadena = cadena + sym
        i = i + 1        

    if request.method =='GET':        
        context = {
            'symptom': cadena,
            'race': disease.race,
            'name': disease.name,
            'answer': disease.answer
        }      
    return render(request,'modal_read.html', context)