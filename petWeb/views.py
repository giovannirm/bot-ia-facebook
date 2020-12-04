#import nltk
#import numpy
#import tflearn
#import tensorflow
#import json
#import pickle
#from nltk.stem.lancaster import LancasterStemmer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Diseases

def home(request):
    return render(request,'home.html')
 
def login(request):    
    if request.method =='POST':                
        user = request.POST['user']
        password = request.POST['password']
        if user == 'root' and password == '123':
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
        #load_variables()
        return redirect('read')         
    return render(request,'add_disease.html')

@csrf_exempt
def update_disease(request):
    id = request.POST.get('id')
    disease = Diseases.objects.get(id = id)
    disease.race = request.POST.get('race').lower()
    disease.name = request.POST.get('name').lower()
    disease.symptom = request.POST.get('symptom').lower().split(', ')
    disease.answer = request.POST.get('answer').lower()
    disease.save()
    #load_variables()
    return redirect('read')
 
def delete_disease(request, id): 
    if request.method == 'GET':
        disease = Diseases.objects.get(id = id)
        disease.delete()
        #load_variables()
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

"""
def load_variables():
    nltk.download('punkt')
    stemmer = LancasterStemmer()
    diseases = Diseases.objects.all()
    palabras = []
    names = []
    auxX = []
    auxY = []      
    for disease in diseases: 
        for symptom in disease.symptom:
            auxPalabra = nltk.word_tokenize(symptom)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(disease.name)        
            if disease.name not in names:            
                names.append(disease.name)

    palabras = [stemmer.stem(w.lower()) for w in palabras if w != "?"]
    palabras = sorted(list(set(palabras)))
    names = sorted(names)
    entrenamiento = []
    salida = []
    salidaVacia = [0 for _ in range(len(names))]

    for x, documento in enumerate(auxX):
        cubeta = []    
        auxPalabra = [stemmer.stem(w.lower()) for w in documento]
        for w in palabras:
            if w in auxPalabra:
                cubeta.append(1)
            else:
                cubeta.append(0)    
        filaSalida = salidaVacia[:]
        filaSalida[names.index(auxY[x])] = 1
        entrenamiento.append(cubeta)
        salida.append(filaSalida)

    entrenamiento = numpy.array(entrenamiento)
    salida = numpy.array(salida)    
    with open("variables.pickle", "wb") as archivoPickle:
        pickle.dump((palabras, names, entrenamiento, salida), archivoPickle)

    tensorflow.compat.v1.reset_default_graph

    red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
    red = tflearn.regression(red)

    modelo = tflearn.DNN(red)
    modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = 10, show_metric = True)
    modelo.save("model.tflearn")   
"""