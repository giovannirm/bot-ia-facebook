import nltk
import numpy
import tflearn
import tensorflow
import json
import pickle

#from flask import request
from django.shortcuts import render, redirect
from .models import Diseases
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from nltk.stem.lancaster import LancasterStemmer
from petWeb.bot import Bot

#nltk.download('punkt')

PAGE_ACCESS_TOKEN = "EAAFYp8VUesEBAAaA1ZC1WCqvIiY09ITJPZBFRdmR6S2H28fPvFfBBTzRNYnF8AnQOXLYBbmg1cWe19DamJmxQZASujNxksZB0zhKHEj7ddWzUx93BrLuBCBYtzlrihzM6tgDGw0pvpU6OFhyQCMwBdZCFlEuhfAZBvNfFKgXBNpEnkWE0qGze0"

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
        load_variables()
        return redirect('read') 
        #return HttpResponse(batch)
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
    load_variables()
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

def load_variables():
    stemmer = LancasterStemmer()
    palabras = []
    names = []
    auxX = []
    auxY = []  
    diseases = Diseases.objects.all()
    for disease in diseases: 
        for symptom in disease.symptom:
            auxPalabra = nltk.word_tokenize(symptom)
            palabras.extend(auxPalabra)
            auxX.append(auxPalabra)
            auxY.append(disease.name)        
            if disease.name not in names:            
                names.append(disease.name)

    batch_size = len(palabras)

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

    tensorflow.reset_default_graph()

    red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
    red = tflearn.regression(red)

    modelo = tflearn.DNN(red)
    modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = batch_size, show_metric = True)
    modelo.save("model.tflearn")   

from flask import request

def webhook(): 
           
    if request.method =='GET':
        VERIFY_TOKEN = "TUTOKENCITOPATUCONSUMO"
        MODE = "subscribe"
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        mode = request.args.get('hub.mode')
        
        if mode and token:
            if mode == MODE and token == VERIFY_TOKEN:            
                print(f"Webhook verificado:\ntoken: {token}\nchallengue: {challenge}\nmode: {mode}")
                return str(challenge)
            else:            
                caso = 'Token equivocado'
                return caso
        else:        
            caso = f"No se estableció [<br>mode: {mode},<br> token: {token} ]<br>Suponemos que abrió la url"
            return caso

    elif request.method =='POST':
        stemmer = LancasterStemmer()

        with open("variables.pickle", "rb") as archivoPickle:
            palabras, names, entrenamiento, salida = pickle.load(archivoPickle)
        
        tensorflow.reset_default_graph()

        red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
        red = tflearn.fully_connected(red, 10)
        red = tflearn.fully_connected(red, 10)
        red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
        red = tflearn.regression(red)

        modelo = tflearn.DNN(red)
        modelo.load("model.tflearn")  

        diseases = Diseases.objects.all()
        data = json.loads(request.data)  

        if data['object'] == 'page':        
            messaging_events = data['entry'][0]['messaging']
            bot = Bot(PAGE_ACCESS_TOKEN)

            for message in messaging_events:
                    
                user_id = message['sender']['id']
                text_input = message['message'].get('text')

                cubeta = [0 for _ in range(len(palabras))]            
                entradaProcesada = nltk.word_tokenize(text_input)
                entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
                    
                for palabraIndividual in entradaProcesada:
                    for i, palabra in enumerate(palabras): 
                        if palabra == palabraIndividual:
                            cubeta[i] = 1

                resultados = modelo.predict([numpy.array(cubeta)])            
                resultadosIndices = numpy.argmax(resultados)
                name = names[resultadosIndices]
                    
                for disease in diseases:
                    if disease.name == name:
                        response_text = disease.answer
                    
                bot.send_text_message(user_id, response_text)
            return 'Exitoso POST'        
        else:
            caso = f"El objecto es de tipo {data['object']}"
            return caso