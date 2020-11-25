import json
import os
'''
biblioteca para el lenguaje de programación Python que da
soporte para crear vectores y matrices grandes multidimensionales,
'''
import numpy
import tflearn
import tensorflow
import random
#Se piensa guardar el modelo de la IA para no estar repitiendo el proceso
#import pickle
#Nos va a permitir procesar el lenguaje
import nltk

from flask import Flask, request
from botFacebook.bot import Bot
from nltk.stem.lancaster import LancasterStemmer
#Definimos un objeto de la clase LancasterStemmer
stemmer = LancasterStemmer()

#para el hosting es necesario tener sin comentar esta parte
#Es un paquete que necesita nltk
nltk.download('punkt')

#PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
PAGE_ACCESS_TOKEN = "asgasgfsa"
#VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
VERIFY_TOKEN = "afasgfasg"
#MODE = os.environ.get('MODE')
MODE = "susbcribe"

#Abrimos la librería de respuestas y preguntas que usará la IA 
with open("botFacebook/contenido.json", encoding = 'utf-8') as archivo:
    datos = json.load(archivo)
    #print(datos)
 
#Se almacenarán las palabras    
palabras = []
tags = []
auxX = []
auxY = []

for contenido in datos["contenido"]:
    for patrones in contenido["patrones"]:
        # nltk nos va a permitir trabajar con el lenguaje natural
        # word_tokenize toma una frase y separa en palabras y reconoce
        # puntos especiales como: ?,., ,!,:, entre otros puntos especiales
        auxPalabra = nltk.word_tokenize(patrones)
        palabras.extend(auxPalabra)
        auxX.append(auxPalabra)
        #auxY Almacena los tag repetidos
        auxY.append(contenido["tag"])

        #Para evitar tener tag repetidos
        if contenido["tag"] not in tags:
            #tags Almacena los tag sin repetir
            tags.append(contenido["tag"])

#print(palabras)
'''
['hola','un','saludo','hello','adios','hasta','la','proxima','nos','vemos']
'''
#print(auxX)
'''    
[['hola'],['un','saludo'],['hello'],['adios'],['hasta','la','proxima'],['nos','vemos']]
'''
#print(auxY)
#['saludo','saludo','saludo','despedida','despedida','despedida']
#print(tags)
#['saludo','despedida']
'''
El método stem es como un casting de palabras para que
sean entendidas por el chatbot
w.lower() es la palabra transformada en minúscula
for w in palabras if w != "?" quiere decir en w en almacenan las 
palabras pero no las que tienen simbolo de ?
'''
palabras = [stemmer.stem(w.lower()) for w in palabras if w != "?"]
#sorted Nos regresa una lista de algo ya ordenado
palabras = sorted(list(set(palabras)))
tags = sorted(tags)

#Aquí se guardará el entrenamiento
entrenamiento = []
salida = []
#Guardamos puros 0 con límite del total de tags
salidaVacia = [0 for _ in range(len(tags))]

#enumerate se encarga de establecer un indice para cada palabra
'''
En x se guarda el indice
En documento se guarda la palabra
Ejemplo
x = 0
documento = hola
'''
for x, documento in enumerate(auxX):
    cubeta = []
    #Va a realizar el casteo como en el anterior
    auxPalabra = [stemmer.stem(w.lower()) for w in documento]
    for w in palabras:
        if w in auxPalabra:
            cubeta.append(1)
        else:
            cubeta.append(0)
    #
    filaSalida = salidaVacia[:]
    filaSalida[tags.index(auxY[x])] = 1
    entrenamiento.append(cubeta)
    salida.append(filaSalida)

#print(entrenamiento)
#print(salida)

entrenamiento = numpy.array(entrenamiento)
salida = numpy.array(salida)
    
#Poner nuestro espacio de trabajo en cero    
#tensorflow.compa.v1.reset_default_graph
tensorflow.reset_default_graph()

red = tflearn.input_data(shape = [None, len(entrenamiento[0])])
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, 10)
red = tflearn.fully_connected(red, len(salida[0]), activation = "softmax")
red = tflearn.regression(red)

modelo = tflearn.DNN(red)
#batch_size es el total de entradas o palabras ese batch_size debe contener un metodo
modelo.fit(entrenamiento, salida, n_epoch = 1000, batch_size = 20, show_metric = True)
modelo.save("modelo.tflearn")
#GREETINGS = ['hola', 'cómo estás', 'buenas']

app = Flask(__name__)

#Creamos la ruta
@app.route('/', methods = ['GET'])
def verify():
    '''
    Necesitamos validar el token para que pueda haber un puente de
    enlace con messenger
    '''
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    mode = request.args.get('hub.mode')

    if mode and token:
        #Este caso se da cuando ingresamos correctamente el token
        if mode == MODE and token == VERIFY_TOKEN:            
            print(f"Webhook verificado:\ntoken: {token}\nchallengue: {challenge}\nmode: {mode}")
            #Este valor se necesita retornar para que FB reciba el valor
            return str(challenge)
        else:
            #Este caso se da cuando ponen un token equivocado
            caso = 'Token equivocado'
            return caso
    else:
        #Este caso se da cuando abrimos la url del hosting
        caso = f"No se estableció [<br>mode: {mode},<br> token: {token} ]<br>Suponemos que abrió la url"
        return caso

# endpoint para procesar los mensajes que llegan
@app.route('/', methods = ['POST'])
def webhook():

    #request.data es la información recibida por el BOT
    print(f"-----------------Información-----------------\n{request.data}\n---------------------------------------------")

    #Guardamos la información de fb en un json
    data = json.loads(request.data)
    
    if data['object'] == 'page':

        #Guardamos los eventos de mensajería
        messaging_events = data['entry'][0]['messaging']
        bot = Bot(PAGE_ACCESS_TOKEN)
        #Entramos a todos los eventos
        for message in messaging_events:
            #Obtenemos el id del emisor
            user_id = message['sender']['id']
            '''
            Obtenemos el texto del emisor
            Ponemos el get debido a que el mensaje puede que sea 
            una imagen y puede que falle el código ya que sino 
            sería ['message']['text']
            '''
            text_input = message['message'].get('text')

            cubeta = [0 for _ in range(len(palabras))]
            #entradaProcesada = nltk.word_tokenize(entrada)
            entradaProcesada = nltk.word_tokenize(text_input)
            entradaProcesada = [stemmer.stem(palabra.lower()) for palabra in entradaProcesada]
            for palabraIndividual in entradaProcesada:
                for i, palabra in enumerate(palabras): 
                    if palabra == palabraIndividual:
                        cubeta[i] = 1
            resultados = modelo.predict([numpy.array(cubeta)])
            #Nos va a regresar el indice q más probabilidad obtuvo
            resultadosIndices = numpy.argmax(resultados)
            tag = tags[resultadosIndices]
            
            for tagAux in datos["contenido"]:
                if tagAux["tag"] == tag:
                    response_text = tagAux["respuestas"]

            #response_text = 'Me encuentro en proceso de aprendizaje 😒'
            #Si el texto ingresado forma parte del array GREETINGS mostrar los sgte
            #if text_input in GREETINGS:
                #response_text = 'Hola. Bienvenido te habla la computadora, decir aua 😁'
            #El format sirve para poner los datos en las llaves
            print('Mensaje del usuario_ID {} - {}'.format(user_id, text_input))
            #bot.send_text_message(user_id, 'Procesando...')
            bot.send_text_message(user_id, random.choice(response_text))
        return 'Exitoso POST'        
    else:
        caso = f"El objecto es de tipo {data['object']}"
        return caso

if __name__ == '__main__':
    app.run(debug = True)    
    
'''
{
    "object":"page",
    "entry":
    [{
        "id":"106501624567068",
        "time":1602749549184,
        "messaging":
        [{
            "sender":
            {
                "id":"3056506177784504"
            },
            "recipient":
            {
                "id":"106501624567068"
            },
            "timestamp":1602749544338,
            "message":
            {
                "mid":"m_yUwR_aaYoRwc_ZaADAGX1PHsxe89Al1BEp0h_VAdMgkJaUfr1vzVsr_OtKuSuxeZbwfT05in4fq5qOvZPEM8Cw",
                "text":"jaja"
            }
        }]
    }]
}
'''