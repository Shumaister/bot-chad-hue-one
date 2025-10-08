import os
from dotenv import load_dotenv
import telebot
import random

load_dotenv()
 
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

import os
from dotenv import load_dotenv
import telebot
from telebot.handler_backends import State, StatesGroup
 
load_dotenv()
 
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("Arriba Bot... boiung bouign ,biip pipi bippo ya estoy andando")

# Handler for new chat members (when bot is added to a group)
@bot.message_handler(content_types=['new_chat_members'])
def welcome_new_members(message):
    for new_member in message.new_chat_members:
        if new_member.id == bot.get_me().id:
            bot.reply_to(message, "¡Hola! Me han agregado al grupo. Estaré leyendo los mensajes 👀")

# Single handler for all messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    # Get message information
    text = message.text
    user_name = message.from_user.first_name
    chat_type = message.chat.type
    
    # Print debug information
    # print(f"Mensaje recibido en {chat_type} de {user_name}: {text}")
    
    # Add group-specific information to responses
    # group_info = f"Grupo: {message.chat.title}" if chat_type in ['group', 'supergroup'] else "Chat privado"
    
    # Check if it's a command
    if text.startswith('/renum'):
        command = text.lower().split()[0]
        if command in ['/renum-start', '/renum-help']:
            bot.reply_to(
                message,
                f"""Hola {user_name}, soy tu bot.
                
                Puedo:
                - Responder a saludos
                - Dar respuestas especiales a números y palabras clave""")
        else:
            bot.reply_to(message, f"Comando {command} no reconocido.")
        return

    # Check if it's a greeting
    if text.lower() in ["hola", "hello", "hi"]:
        bot.reply_to(message, f"Tu nariz contra mis bolas. Ahora si, Hola {user_name}! ¿En qué te puedo ayudar?")
        return

    # Check if the message ends with a number
    last_word = text.split()[-1]
    if last_word == "5":
        bot.reply_to(message, "POR EL CULO TE LA HINCO")
        return
    
    if last_word == "13":
        bot.reply_to(message, lookup_phrases(last_word))
        return
    
    if last_word == "4":
        bot.reply_to(message, lookup_phrases(last_word))
        return

    if last_word == "8":
        bot.reply_to(message, "EL CULO TE ABROCHO")
        return

    if last_word == "9":
        bot.reply_to(message, "EL CULO TE LLUEVE")
        return

    if last_word == "12":
        bot.reply_to(message, "SI TE ROMPO EL CULO QUIEN TE LO COSE")
        return

    if last_word == "11":
        bot.reply_to(message, "CHUPALO ENTONCE")
        return
    
    # Check if message contains specific word
    if "fabio" in text or "Fabio" in text:
        bot.reply_to(message, "Es con V corta irrespetuoso de mierda. Ta bien que es oscuro pero pará...")
        return

    # For any other text, provide word and character count
    # words = len(text.split())
    # chars = len(text)
    # bot.reply_to(
    #     message,
    #     f"Tu mensaje tiene {words} palabras y {chars} caracteres."
    # )

def lookup_phrases(number):
    diccionary_phrase = { 
        "4":    ["El culo te parto", "Te puse", "La ponen", "Allá", "Te puse"],
        "13":   ["Más me la mamas más me crece", "Agarrá LA que me crece", "while true: me crece"]
    }   
    esto = random.choice(diccionary_phrase[number])
    return esto

# Start the bot
bot.polling()
