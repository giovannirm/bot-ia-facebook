import requests
import json
import os

#FACEBOOK_GRAPH_URL = os.environ.get('FACEBOOK_GRAPH_URL')
#CONTENT_TYPE = os.environ.get('CONTENT_TYPE')
FACEBOOK_GRAPH_URL = "https://graph.facebook.com/v2.6/me/"
CONTENT_TYPE = "application/json"


class Bot(object):
    def __init__(self, access_token, api_url=FACEBOOK_GRAPH_URL):
        self.access_token = access_token
        self.api_url = api_url

    # Enviamos el mensaje
    def send_text_message(self, psid, message, messaging_type="RESPONSE"):
        headers = {
            'Content-Type': CONTENT_TYPE
        }

        data = {
            'messaging_type': messaging_type,
            'recipient': {
                'id': psid
            },
            'message': {
                'text': message,
            }
        }

        params = {
            'access_token': self.access_token
        }

        self.api_url = self.api_url + 'messages'
        # Enviamos una solicitud de publicación
        response = requests.post(self.api_url,
                                 headers=headers,
                                 params=params,
                                 data=json.dumps(data))
        print(response.content)

    def send_text_confirmation(self, psid, messaging_type="RESPONSE"):
        headers = {
            'Content-Type': CONTENT_TYPE
        }

        data = {
            'messaging_type': messaging_type,
            'recipient': {
                'id': psid
            },
            'message': {
                "attachment": {
                    "type": "template",
                    "payload": {
                        "template_type": "generic",
                        "elements": [
                            {
                                "title": "Estás seguro de realizar la consulta?",
                                "image_url": 'https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fbemoralzarzal.com%2Fwp-content%2Fuploads%2F2019%2F04%2FCentro-Veterinario-Fuente-del-Moral-en-Moralzarzal-conulta-848x566-848x566.jpg&f=1&nofb=1',                                
                                "buttons": [
                                    {
                                        "type": "postback",
                                        "title": "Sí",
                                        "payload": "yes"
                                    }, {
                                        "type": "postback",
                                        "title": "No",
                                        "payload": "no"
                                    }
                                ]
                            }
                        ]
                    }
                }
            }
        }

        params = {
            'access_token': self.access_token
        }

        self.api_url = self.api_url + 'messages'
        # Enviamos una solicitud de publicación
        response = requests.post(self.api_url,
                                 headers=headers,
                                 params=params,
                                 data=json.dumps(data))
