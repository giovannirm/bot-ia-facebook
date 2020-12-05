import nltk
import numpy
import tflearn
import tensorflow
import json
import pickle
import os
from nltk.stem.lancaster import LancasterStemmer
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Diseases

from django.views import generic
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
#from django.views.decorators.cache import never_cache
from django.http.response import HttpResponse
from petBot.bot import Bot

nltk.download('punkt')

tags = ['saludo', 'despedida', 'consulta']
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
MODE = os.environ.get('MODE')
PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')

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
        load_variables()
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
    load_variables()
    return redirect('read')
 
def delete_disease(request, id): 
    if request.method == 'GET':
        disease = Diseases.objects.get(id = id)
        disease.delete()
        load_variables()
    return redirect('read')    

def read_diseases(request):
    diseases = Diseases.objects.all()        
    context = {
        'diseases': diseases,
        'tags': tags,
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

    tensorflow.compat.v1.reset_default_graph()
    #tensorflow.reset_default_graph()

    red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
    red = tflearn.regression(red)

    modelo = tflearn.DNN(red)
    modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = 10, show_metric = True)
    modelo.save("model.tflearn")   

class Webhook(generic.View):
    def get(self, request, *args, **kwargs):
        #VERIFY_TOKEN = "TUTOKENCITOPATUCONSUMO"   
        #MODE = "subscribe"
        token = request.GET['hub.verify_token']               
        challenge = request.GET['hub.challenge']
        mode = request.GET['hub.mode']

        if mode and token:
            if mode == MODE and token == VERIFY_TOKEN:            
                print(f"Webhook verificado:\ntoken: {token}\nchallengue: {challenge}\nmode: {mode}")            
                return HttpResponse(challenge)
            else:            
                return HttpResponse('Token equivocado')
        else:        
            caso = f"No se estableció [<br>mode: {mode},<br> token: {token} ]<br>Suponemos que abrió la url"
            return HttpResponse(caso)

    #@method_decorator(never_cache)
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return generic.View.dispatch(self, request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        #PAGE_ACCESS_TOKEN = "EAAFwexrc6MMBAKpQOsjgExNHXjH5wc3OgRtIweZC8ZChzUhET9EZBLIAzUJqIWI2yutciZBuSMZAW17zRt8ODsMfMt0J34uuRVTNhFJcXv96qe9OobpZCATwpDBCnzemqiN9z704bnUv8wpt2yVy4AGlltrP7KpZC0ZBXhU3GxiZAyOJfUQLZA2OZBl"    	    
        stemmer = LancasterStemmer()
        diseases = Diseases.objects.all()
        
        with open("variables.pickle", "rb") as archivoPickle:
            palabras, names, entrenamiento, salida = pickle.load(archivoPickle)
        
        tensorflow.compat.v1.reset_default_graph()
        #tensorflow.reset_default_graph()

        red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
        red = tflearn.fully_connected(red, 10)
        red = tflearn.fully_connected(red, 10)
        red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
        red = tflearn.regression(red)

        modelo = tflearn.DNN(red)
        modelo.load("model.tflearn") 

        data = json.loads(self.request.body.decode('utf-8'))
        print(data)
        bot = Bot(PAGE_ACCESS_TOKEN)

        if data['object'] == 'page':   
            messaging_events = data['entry'][0]['messaging']  
            for message in messaging_events:                
                user_id = message['sender']['id']                 
                if 'message' in message:
                    if 'text' in message['message']:              
                        text_input = message['message']['text']
                        print('Mensaje del usuario_ID {} - {}'.format(user_id, text_input))
                        
                        cubeta = [0 for _ in range(len(palabras))]            
                        entradaProcesada = nltk.word_tokenize(text_input)
                        entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
                            
                        for palabraIndividual in entradaProcesada:
                            for i, palabra in enumerate(palabras): 
                                if palabra == palabraIndividual:
                                    cubeta[i] = 1

                        #print(cubeta)
                        resultados = modelo.predict([numpy.array(cubeta)])            
                        resultadosIndices = numpy.argmax(resultados)
                        name = names[resultadosIndices]
                        #print(name)
                        #response_text = ""

                        if name not in tags: 
                            for disease in diseases:                                                
                                if disease.name == name:
                                    response_text = "La enfermedad de su can es " + disease.name + ", " + disease.answer                    
                                    bot.send_text_message(user_id, response_text)                            
                        else:
                            if name == 'consulta':
                                bot.send_text_confirmation(user_id)
                            else:
                                for disease in diseases:
                                    if disease.name == name:
                                        response_text = disease.answer
                                        bot.send_text_message(user_id, response_text)                            
                    else:                    
                        response_text = "Disculpa pero creo que aún no soy tan inteligente como para entenderte 😢"
                        bot.send_text_message(user_id, response_text)                          
                else:
                    payload = message['postback']['payload']
                    if payload == 'yes':
                        response_text = "Necesito que me digas los síntomas de tu can para poder darle un posible diagnóstico"
                        bot.send_text_message(user_id, response_text)                                                  
                    elif payload == 'no':
                        response_text = "Por ahora solo cuento con la función de diagnosticar canes, en algún futuro podré tener más conocimientos y te ofreceré más de mis funciones 🤞"
                        bot.send_text_message(user_id, response_text)                          
            return HttpResponse('Exitoso POST')
        else:
            caso = f"El objecto es de tipo {data['object']}"
            return HttpResponse(caso)  