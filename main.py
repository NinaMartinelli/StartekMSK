import os
import telebot
from telebot import types
import requests
import time

# Establece el token directamente para pruebas
os.environ['TOKEN'] = "6782919923:AAGE4n20pIXTb21cXYAI-oH13K0si6usKEA"

# Obtén el token del bot desde las variables de entorno
TOKEN = os.getenv('TOKEN')
print(f"TOKEN: {TOKEN}")  # Línea de depuración
if TOKEN is None:
    raise ValueError("No se ha encontrado el token del bot en las variables de entorno.")

# Inicializa el bot
bot = telebot.TeleBot(TOKEN)

# Manejador del comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Tengo una consulta')
    btn2 = types.KeyboardButton('Gestionar mis métricas')
    btn3 = types.KeyboardButton('Accesos directos')
    btn4 = types.KeyboardButton('Hacer una sugerencia')
    btn5 = types.KeyboardButton('Quiero postular mi llamada')
    btn6 = types.KeyboardButton('Volver atrás')
    markup.add(btn1, btn2, btn3, btn4, btn5, btn6)
    
    bot.send_message(message.chat.id, "¡Bienvenido! Selecciona una opción:", reply_markup=markup)

# Manejador del comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Puedes interactuar conmigo usando comandos. Por ahora solo respondo a /start y /help')

# Manejador de mensajes
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Tengo una consulta':
        handle_consultas(message)
    elif message.text == 'Gestionar mis métricas':
        bot.send_message(message.chat.id, "Gestiona tus métricas aquí: [Gestionar mis métricas](https://santirojo.github.io/calculamsk/)", parse_mode="Markdown")
    elif message.text == 'Accesos directos':
        handle_accesos_directos(message)
    elif message.text == 'Hacer una sugerencia':
        handle_sugerencias(message)
    elif message.text == 'Quiero postular mi llamada':
        handle_postular_llamada(message)
    elif message.text == 'Volver atrás':
        send_welcome(message)
    else:
        bot.reply_to(message, "Opción no válida, por favor selecciona una opción del menú.")

def handle_consultas(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn_si = types.InlineKeyboardButton('Sí', callback_data='Consultas_si')
    btn_no = types.InlineKeyboardButton('No', callback_data='Consultas_no')
    btn_back = types.InlineKeyboardButton('Volver atrás', callback_data='back')
    markup.add(btn_si, btn_no, btn_back)
    bot.send_message(message.chat.id, "¿Te ayudo con tu llamada?", reply_markup=markup)

def handle_accesos_directos(message):
    bot.send_message(message.chat.id, "Accesos directos:\n1. Google: https://www.google.com\n2. GitHub: https://www.github.com")

def handle_sugerencias(message):
    bot.send_message(message.chat.id, "Por favor, envía tu sugerencia y la revisaremos pronto.")

def handle_postular_llamada(message):
    bot.send_message(message.chat.id, "Para postular tu llamada, por favor sigue las instrucciones:\n1. Describe tu llamada.\n2. Envía los detalles relevantes.")

# Manejador de consultas (Inline Keyboard)
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Consultas_si':
        bot.answer_callback_query(call.id, 'Has seleccionado "Sí"')
    elif call.data == 'Consultas_no':
        bot.answer_callback_query(call.id, 'De acuerdo, no hay problema.')
    elif call.data == 'back':
        bot.send_message(call.message.chat.id, "Volviendo al menú principal...")
        send_welcome(call.message)

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
        