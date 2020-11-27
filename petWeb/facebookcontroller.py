import json
import os
import numpy
import tflearn
import tensorflow
import random
import nltk

from flask import Flask, request
from petWeb.bot import Bot
from nltk.stem.lancaster import LancasterStemmer
from .models import Diseases

stemmer = LancasterStemmer()
nltk.download('punkt')


PAGE_ACCESS_TOKEN = "EAAFYp8VUesEBAAaA1ZC1WCqvIiY09ITJPZBFRdmR6S2H28fPvFfBBTzRNYnF8AnQOXLYBbmg1cWe19DamJmxQZASujNxksZB0zhKHEj7ddWzUx93BrLuBCBYtzlrihzM6tgDGw0pvpU6OFhyQCMwBdZCFlEuhfAZBvNfFKgXBNpEnkWE0qGze0"
VERIFY_TOKEN = "TUTOKENCITOPATUCONSUMO"
MODE = "subscribe"

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
            names.append(disease.names)

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
tensorflow.reset_default_graph()

red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
red = tflearn.regression(red)

modelo = tflearn.DNN(red)
modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = 20, show_metric = True)
modelo.save("model.tflearn")

app = Flask(__name__)

def verify():
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



def webhook():    
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
                if disease["name"] == name:
                    response_text = disease.answer
            
            bot.send_text_message(user_id, random.choice(response_text))
        return 'Exitoso POST'        
    else:
        caso = f"El objecto es de tipo {data['object']}"
        return caso
        
if __name__ == '__main__':
    app.run(debug = True)    