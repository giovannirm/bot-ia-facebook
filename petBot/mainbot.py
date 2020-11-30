'''
biblioteca para el lenguaje de programación Python que da
soporte para crear vectores y matrices grandes multidimensionales,
'''
import numpy
import json
import tflearn
import tensorflow
import nltk
#Se piensa guardar el modelo de la IA para no estar repitiendo el proceso
import pickle
from pymongo import MongoClient
from flask import Flask, request
from bot import Bot
from nltk.stem.lancaster import LancasterStemmer

app = Flask(__name__)

#app.config['MONGO_URI'] = ''

nltk.download('punkt')
stemmer = LancasterStemmer()
client = MongoClient("mongodb+srv://petvillano:123@cluster.abnui.mongodb.net/pet?retryWrites=true&w=majority")

PAGE_ACCESS_TOKEN = "EAAJm7lO5XNsBAAcF3TiOHj93yDiQSZBY7E7SshtRbEqc2bhnPcP5aCB5186xi0t099s1ikdyNsxEVRUIgr2oz20EBOkQvZAZC7EuZACMucqowVAIrTptbd0Prxn3MfeYZCghdl8YwH6JIRfJxbcSNfun1pQWrFBrwJ2qAfrg3Fhp9VFPRKpND"
VERIFY_TOKEN = "TUTOKENCITOPATUCONSUMO"
MODE = "subscribe"

db = client['pet']
col = db['diseases']
#diseases = col.find({})

#with open("variables.pickle", "rb") as archivoPickle:
#    palabras, names, entrenamiento, salida = pickle.load(archivoPickle)
"""
palabras = []
names = []
auxX = []
auxY = []  

for disease in diseases: 
    for symptom in disease['symptom']:
        #print(f"síntoma: {symptom}")
        auxPalabra = nltk.word_tokenize(symptom)
        #print(f"auxPalabra: {auxPalabra}")
        palabras.extend(auxPalabra)
        #print(f"palabras: {palabras}")
        auxX.append(auxPalabra)
        #print(f"auxX: {auxX}")
        auxY.append(disease['name'])        
        #print(f"auxY: {auxY}")
        if disease['name'] not in names:                        
            names.append(disease['name'])
            #print(f"names: {names}")

#batch_size = len(palabras)
#el stem es para derivar semánticamente las palabras
palabras = [stemmer.stem(w.lower()) for w in palabras if w != "?"]
#print(f"palabras: {palabras}")
palabras = sorted(list(set(palabras)))
#print(f"palabras.sorted: {palabras}")
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

#convertiremos nuestros datos de entrenamiento y salida a matrices numpy
entrenamiento = numpy.array(entrenamiento)
salida = numpy.array(salida)    

#with open("variables.pickle", "rb") as archivoPickle:
#    palabras, names, entrenamiento, salida = pickle.load(archivoPickle)
"""
"""
tensorflow.compat.v1.reset_default_graph
#tensorflow.reset_default_graph()

red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
red = tflearn.regression(red)

modelo = tflearn.DNN(red)
modelo.fit(entrenamiento, salida, n_epoch = 2000, batch_size = 10, show_metric = True)
#modelo.load("modelo.tflearn")
"""


@app.route('/webhook', methods = ['GET'])
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

@app.route('/webhook', methods = ['POST'])
def webhook():    
    
    stemmer = LancasterStemmer()
    diseases = col.find({})
    #print(request.data)
    with open("../variables.pickle", "rb") as archivoPickle:
        palabras, names, entrenamiento, salida = pickle.load(archivoPickle)
    #print(palabras)
    tensorflow.compat.v1.reset_default_graph
    #tensorflow.reset_default_graph()

    red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, 10)
    red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
    red = tflearn.regression(red)

    modelo = tflearn.DNN(red)
    modelo.load("../model.tflearn") 

    data = json.loads(request.data)
    
    if data['object'] == 'page':        
        messaging_events = data['entry'][0]['messaging']
        bot = Bot(PAGE_ACCESS_TOKEN)

        for message in messaging_events:
            
            user_id = message['sender']['id']            
            #text_input = message['message'].get('text')
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
            response_text = ""

            for disease in diseases:
                if disease['name'] == name:
                    response_text = disease['name'] ": "+ disease['answer']
            #print(response_text)
            bot.send_text_message(user_id, response_text)
        return 'Exitoso POST'        
    else:
        caso = f"El objecto es de tipo {data['object']}"
        return caso
        
#Esto es para que la app se ejecute cada vez que hay un cambio
if __name__ == '__main__':
    app.run(debug = True)    