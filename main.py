import os
import telebot
from telebot import types
import requests
import time
import signal

# Establece el token directamente para pruebas
os.environ['TOKEN'] = "6782919923:AAGE4n20pIXTb21cXYAI-oH13K0si6usKEA"

# Obtén el token del bot desde las variables de entorno
TOKEN = os.getenv('TOKEN')
if TOKEN is None:
    raise ValueError("No se ha encontrado el token del bot en las variables de entorno.")

# Inicializa el bot
bot = telebot.TeleBot(TOKEN)
# URL de la API para obtener el permiso
PERMISSION_API_URL = "https://apimocha.com/nominamsk/nomina"

# Función para solicitar permiso
def request_permission():
    try:
        response = requests.get(PERMISSION_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get("permitido", False)
        else:
            return False
    except requests.RequestException as e:
        print(f"Error al conectar con la API: {e}")
        return False

# Función para preguntar cómo se siente el usuario
def ask_how_are_you(message):
    markup = types.ReplyKeyboardMarkup(row_width=3, one_time_keyboard=True)
    joy = types.KeyboardButton('😃')
    sadness = types.KeyboardButton('😢')
    neutral = types.KeyboardButton('😐')
    fear = types.KeyboardButton('😱')
    anger = types.KeyboardButton('😡')
    markup.add(joy, sadness, neutral, fear, anger)
    bot.send_message(message.chat.id, "¿Cómo te sientes hoy?", reply_markup=markup)

# Manejador del comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if request_permission():
        ask_how_are_you(message)
    else:
        bot.send_message(message.chat.id, "No tienes permiso para usar este bot.")

# Manejador de las respuestas a la pregunta "¿Cómo te sientes hoy?"
@bot.message_handler(func=lambda message: message.text in ['😃', '😢', '😐', '😱', '😡'])
def handle_feelings(message):
    feeling_responses = {
        '😃': '¡Me alegra saber que te sientes feliz!',
        '😢': 'Lo siento, espero que te sientas mejor pronto.',
        '😐': 'Entiendo, todos tenemos días neutrales. ¡Vamos a intentar un cambio de actitud!',
        '😱': 'Debe ser difícil sentir miedo, pero confía en tus acciones y tendrás buen desempeño.',
        '😡': 'Intenta cambiar esa energía con pensamientos positivos y buscando la solución o alternativa que tengas para brindar.'
    }
    response = feeling_responses.get(message.text, "Gracias por compartir cómo te sientes.")
    bot.send_message(message.chat.id, response)
    # Luego de recibir la respuesta, mostramos el menú principal
    show_main_menu(message)

def show_main_menu(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Tengo una consulta')
    btn2 = types.KeyboardButton('Gestionar mis métricas')
    btn3 = types.KeyboardButton('Accesos directos')
    btn4 = types.KeyboardButton('Hacer una sugerencia')
    btn5 = types.KeyboardButton('Quiero postular mi llamada')
    btn6 = types.KeyboardButton('Volver atrás')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    bot.send_message(message.chat.id, "¡Bienvenido! Selecciona una opción:", reply_markup=markup)

# Manejador de texto para cambiar el menú cuando se presiona 'Tengo una consulta'
@bot.message_handler(func=lambda message: message.text == 'Tengo una consulta')
def handle_consultas(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn1 = types.KeyboardButton('¿Cómo cargo un ajuste?')
    btn2 = types.KeyboardButton('¿Como cargo un ajuste de una línea cancelada?')
    btn3 = types.KeyboardButton('¿Cómo cargo ajuste de una línea cancelada si no me sale el NIM en pec o no tiene otra cuenta activa?')
    btn4 = types.KeyboardButton('¿Cómo solicitar soporte técnico?')
    btn_back = types.KeyboardButton('Atrás')
    markup.add(btn1, btn2, btn3, btn4, btn_back)
    
    bot.send_message(message.chat.id, "Selecciona tu consulta:", reply_markup=markup)

# Manejador de las consultas específicas
@bot.message_handler(func=lambda message: message.text in [
    '¿Cómo cargo un ajuste?',
    '¿Cómo cargo un ajuste de una línea cancelada?',
    '¿Cómo cargo ajuste de una línea cancelada si no me sale el NIM en pec o no tiene otra cuenta activa?',
    'Cambio de sim - FRAUDE'
])
def handle_specific_consultas(message):
    responses = {
        '¿Cómo cargo un ajuste?':'Todos los ajustes se cargan por PEC, tenés que validar el motivo que genera el ajuste para determinar si corresponde o no. Podes ver motivos en https://claroaup.sharepoint.com/sites/ClaroPedia2/SitePages/Instructivos/Ajustes---Multiskill.aspx',
        '¿Cómo cargo un ajuste de una línea cancelada?': 'Siempre deben cargarse a través de PEC utilizando el número de cuenta o alguna línea activa o cancelada con número no borrado. Recordar aclarar dentro del pedido los datos de la cuenta a ajustar.',
        '¿Cómo cargo ajuste de una línea cancelada si no me sale el NIM en pec o no tiene otra cuenta activa?': 'Lo debes cargar a través de SMAX- SOLICITUDES CALL CENTER - LOYALTY.',
        'Cambio de sim - FRAUDE': """Cliente inicia la conversación diciendo que se quedó sin línea de golpe o recibió un SMS o mail informando que se hizo un cambio de SIM y desconoce.
        SMS: “Pediste un nuevo chip Claro para tu línea y será entregado en breve. Si vos no lo solicitaste contáctanos en claro.com.ar/chatonline” y no solicitó un cambio de sim.
        Informale que por su seguridad vas a suspender la línea.
        VALIDA DNI.
        SUSPENDE X ROBO.
        CARGA TICKLER DESIM.
        GESTIONA ENVIO CHIP."""
    }
    response = responses.get(message.text, "Consulta no reconocida.")
    bot.send_message(message.chat.id, response)

# Manejador de texto para mostrar el botón "Cambios de horarios" y "Horarios de Break" cuando se presiona 'Accesos directos'
@bot.message_handler(func=lambda message: message.text == 'Accesos directos')
def handle_accesos_directos(message):
    markup = types.ReplyKeyboardMarkup(row_width=1)
    btn_cambios_horarios = types.KeyboardButton('Cambios de horarios')
    btn_horarios_break = types.KeyboardButton('Horarios de Break')
    btn_back = types.KeyboardButton('Atrás')
    markup.add(btn_cambios_horarios, btn_horarios_break, btn_back)
    
    bot.send_message(message.chat.id, "Selecciona una opción:", reply_markup=markup)

# Manejador de texto para mostrar el enlace cuando se presiona 'Cambios de horarios'
@bot.message_handler(func=lambda message: message.text == 'Cambios de horarios')
def handle_cambios_horarios(message):
    link = "https://startek-my.sharepoint.com/:x:/r/personal/romina_lima_startek_com/_layouts/15/Doc.aspx?sourcedoc=%7B85086e59-f869-44e3-ba0a-a44fd58c903c%7D&action=editnew&wdsle=0&wdOrigin=OUTLOOK-METAOS.FILEBROWSER.FILES-FOLDER"
    bot.send_message(message.chat.id, f"Cambios de horarios: [Haz clic aquí]({link})", parse_mode="Markdown")

# Manejador de texto para mostrar el enlace cuando se presiona 'Horarios de Break'
@bot.message_handler(func=lambda message: message.text == 'Horarios de Break')
def handle_horarios_break(message):
    link = "https://startek-my.sharepoint.com/:x:/p/emilse_gonzalez/ES71DlOHk7tBv7x8IZGZZSIB31kQnDPZiSvU2G50aYzQvg"
    bot.send_message(message.chat.id, f"Horarios de Break: [Haz clic aquí]({link})", parse_mode="Markdown")

# Manejador para el botón 'Atrás' que vuelve al menú principal
@bot.message_handler(func=lambda message: message.text == 'Atrás')
def go_back(message):
    show_main_menu(message)

# Manejador de consultas (Inline Keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith('consulta_'):
        consulta_num = call.data.split('_')[1]
        if consulta_num == "1":
            bot.answer_callback_query(call.id, 'Has seleccionado Ajustes')
            bot.send_message(call.message.chat.id, 'Has seleccionado Ajustes. Aquí está la información correspondiente.')
        else:
            bot.answer_callback_query(call.id, f'Has seleccionado la Consulta {consulta_num}')
            bot.send_message(call.message.chat.id, f'Has seleccionado la Consulta {consulta_num}. Aquí está la información correspondiente.')
    elif call.data == 'back':
        show_main_menu(call.message)
    else:
        bot.answer_callback_query(call.id, "Opción no reconocida.")
        bot.send_message(call.message.chat.id, "Opción no reconocida. Por favor, intenta de nuevo.")

def shutdown_bot(signum, frame):
    bot.stop_polling()
    exit(0)

signal.signal(signal.SIGINT, shutdown_bot)
signal.signal(signal.SIGTERM, shutdown_bot)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=40, long_polling_timeout=20)
        except requests.exceptions.ReadTimeout:
            print("ReadTimeout: La solicitud a la API de Telegram ha superado el tiempo de espera.")
            time.sleep(15)  # Espera 15 segundos antes de intentar nuevamente
        except requests.exceptions.ConnectionError:
            print("ConnectionError: Problema de conexión.")
            time.sleep(15)  # Espera 15 segundos antes de intentar nuevamente
        except Exception as e:
            print(f"Ha ocurrido un error inesperado: {e}")
            time.sleep(15)  # Espera 15 segundos antes de intentar nuevamente
