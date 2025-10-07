import os
from dotenv import load_dotenv
import telebot
import random

load_dotenv()
 
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
if not TELEGRAM_TOKEN:
    raise ValueError("No TELEGRAM_TOKEN found in .env file")

bot = telebot.TeleBot(TELEGRAM_TOKEN)

print("Arriba Bot... boiung bouign ,biip pipi bippo ya estoy andando")

# Single handler for all messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    text = message.text
    user_name = message.from_user.first_name
    
    # Check if it's a command
    if text.startswith('/'):
        command = text.lower().split()[0]
        if command in ['/start', '/help']:
            bot.reply_to(
                message,
                f"""Hola {user_name}, soy tu bot. Puedo:
                - Contar palabras y caracteres de cualquier texto
                - Responder a saludos
                - Dar respuestas especiales a números""")
        else:
            bot.reply_to(message, f"Comando {command} no reconocido.")
        return

    # Check if it's a greeting
    if text.lower() in ["hola", "hello", "hi"]:
        bot.reply_to(message, f"Tu nariz contra mis boldas. Ahora si, Hola {user_name}! ¿En qué te puedo ayudar?")
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
    
    # Check if message contains specific word
    if "gasponce" in text or "gaspOnce" in text:
        bot.reply_to(message, "A ESE LO CANCELARON EN TWITTER 2023 POR VIOLIN")
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
        "4":    ["El culo te parto", "Te puse", "La ponen", "Alla", "Te puse"],
        "13":   ["Mas me mamas mas me crece", "Agarra LA que me crece", "while true: me crece"]
    }   
    esto = random.choice(diccionary_phrase[number])
    return esto

# Start the bot
bot.polling()