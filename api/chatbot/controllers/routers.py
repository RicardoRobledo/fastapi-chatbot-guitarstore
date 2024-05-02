from fastapi import APIRouter, Request

from ..services.chatbot_service import ChatbotService

import json


router = APIRouter(prefix='/chatbot/msg', tags=['Chatbot'])

@router.post('')
async def get_users(request:Request):

    metodo = request.method
    
    # Obtener la URL completa de la solicitud
    url = str(request.url)
    
    # Obtener los datos del cuerpo de la solicitud (si los hay)
    datos_cuerpo = await request.body()
    datos_json = json.loads(datos_cuerpo.decode("utf-8"))

    message = datos_json['message']

    # Obtener las cabeceras de la solicitud
    cabeceras = request.headers
    
    # Obtener la dirección IP del cliente que realizó la solicitud
    direccion_ip_cliente = request.client.host
    
    # Puedes imprimir o hacer lo que necesites con esta información
    #print("Método:", metodo)
    #print("URL:", url)
    #print("Parámetros de consulta:", parametros_query)
    #print("Datos del cuerpo:", datos_cuerpo)
    #print("Cabeceras:", cabeceras)
    #print("Dirección IP del cliente:", direccion_ip_cliente)

    msg = await ChatbotService().post_user_message(message)

    return msg
