from flask import Flask, request
from bot import Bot

import json
import os

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
VERIFY_TOKEN = os.environ.get('VERIFY_TOKEN')
MODE = os.environ.get('MODE')

GREETINGS = ['hola', 'cómo estás', 'buenas']

app = Flask(__name__)

#if produccion = 'desarrollador':

#elif produccion = 'hosting':


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
            response_text = 'Me encuentro en proceso de aprendizaje 😒'
            #Si el texto ingresado forma parte del array GREETINGS mostrar los sgte
            if text_input in GREETINGS:
                response_text = 'Hola. Bienvenido te habla la computadora, decir aua 😁'
            #El format sirve para poner los datos en las llaves
            print('Mensaje del usuario_ID {} - {}'.format(user_id, text_input))
            #bot.send_text_message(user_id, 'Procesando...')
            bot.send_text_message(user_id, response_text)
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