import telebot # type: ignore
from telebot import types

# Conexión con nuestro BOT
TOKEN = '6782919923:AAGyiXLvnUEnBwPUye8TvQDQbi1qqoBkEX0'
bot = telebot.TeleBot(TOKEN)

# Manejador del comando /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(row_width=2)
    btn1 = types.KeyboardButton('Consultas')
    btn2 = types.KeyboardButton('Metricas')
    btn3 = types.KeyboardButton('Accesos directos')
    btn4 = types.KeyboardButton('Tengo una sugerencia')
    btn5 = types.KeyboardButton('Quiero postular mi llamada')
    markup.add(btn1, btn2, btn3, btn4, btn5)
    
    bot.send_message(message.chat.id, "Bienvenido! Selecciona una opción:", reply_markup=markup)

# Manejador del comando /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, 'Puedes interactuar conmigo usando comandos. Por ahora solo respondo a /start y /help')

# Manejador de mensajes
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    if message.text == 'Consultas':
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_si = types.InlineKeyboardButton('Si', callback_data='Consultas_si')
        btn_no = types.InlineKeyboardButton('No', callback_data='Consultas_no')
        btn_back = types.InlineKeyboardButton('Volver atrás', callback_data='back')
        markup.add(btn_si, btn_no, btn_back)
        bot.send_message(message.chat.id, "¿Te ayudo con tu llamada?", reply_markup=markup)
    elif message.text == 'Metricas':
        bot.reply_to(message, "Has seleccionado Métricas")
    elif message.text == 'Accesos directos':
        bot.reply_to(message, "Has seleccionado Accesos directos")
    elif message.text == 'Tengo una sugerencia':
        bot.reply_to(message, "Has seleccionado Tengo una sugerencia")
    elif message.text == 'Quiero postular mi llamada':
        bot.reply_to(message, "Has seleccionado Quiero postular mi llamada")
    elif message.text == 'Volver atrás':
        send_welcome(message)
    else:
        bot.reply_to(message, "Opción no válida, por favor selecciona una opción del menú.")

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
    bot.polling(none_stop=True)
