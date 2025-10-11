import os
import time
from dotenv import load_dotenv
import telebot
import random
from telebot.handler_backends import State, StatesGroup

class TelegramBot:
    def __init__(self):
        self.bot = None
        self.setup_bot()
        self.setup_handlers()
    
    def setup_bot(self):
        load_dotenv()
        
        TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
        if not TELEGRAM_TOKEN:
            raise ValueError("No TELEGRAM_TOKEN found in .env file")
        
        self.bot = telebot.TeleBot(TELEGRAM_TOKEN)
        print("Arriba Bot... boiung bouign ,biip pipi bippo ya estoy andando")
    
    def setup_handlers(self):
        @self.bot.message_handler(content_types=['new_chat_members'])
        def welcome_new_members(message):
            try:
                for new_member in message.new_chat_members:
                    if new_member.id == self.bot.get_me().id:
                        self.bot.reply_to(message, "¡Hola! Me han agregado al grupo. Estaré leyendo los mensajes 👀")
            except Exception as e:
                print(f"Error en welcome_new_members: {str(e)}")
        
        @self.bot.message_handler(func=lambda message: True)
        def handle_all_messages(message):
            try:
                # Get message information
                text = message.text
                user_name = message.from_user.first_name
                chat_type = message.chat.type
                
                # Add group-specific information to responses
                group_info = f"Grupo: {message.chat.title}" if chat_type in ['group', 'supergroup'] else "Chat privado"
                
                # Check if it's a command
                if text.startswith('/renum'):
                    command = text.lower().split()[0]
                    if command in ['/renum-start', '/renum-help']:
                        self.bot.reply_to(
                            message,
                            f"""Hola {user_name}, soy tu bot.
                            {group_info}
                            
                            Puedo:
                            - Responder a saludos
                            - Dar respuestas especiales a números y palabras clave""")
                    else:
                        self.bot.reply_to(message, f"Comando {command} no reconocido.")
                    return

                # Check if it's a greeting
                if text.lower() in ["hola", "hello", "hi"]:
                    self.bot.reply_to(message, f"Tu nariz contra mis bolas. Ahora si, Hola {user_name}! ¿En qué te puedo ayudar?")
                    return

                # Check if the message ends with a number
                last_word = text.split()[-1]
                if last_word == "5":
                    self.bot.reply_to(message, "POR EL CULO TE LA HINCO")
                    return
                
                if last_word == "13":
                    self.bot.reply_to(message, self.lookup_phrases(last_word))
                    return
                
                if last_word == "4":
                    self.bot.reply_to(message, self.lookup_phrases(last_word))
                    return
                                                    
            except Exception as e:
                print(f"Error procesando mensaje: {str(e)}")
                print(f"Mensaje que causó el error: {message.text}")


    def run(self):
        while True:
            try:
                print("Bot listo y escuchando mensajes...")
                self.bot.polling(non_stop=True, interval=2)
            except Exception as e:
                print(f"Error crítico del bot: {str(e)}")
                print("Reintentando en 10 segundos...")
                time.sleep(10)
                self.setup_bot()  # Recreate bot instance
                
    def lookup_phrases(self, number):
        diccionary_phrase = { 
            "4":    ["El culo te parto", "Te puse", "La ponen", "Alla", "Te puse"],
            "13":   ["Mas me la mamas mas me crece", "Agarra LA que me crece", "while true: me crece"]
        }   
        return random.choice(diccionary_phrase[number])
    
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
        "13":   ["Mas me la mamas mas me crece", "Agarra LA que me crece", "while true: me crece"]
    }   
    esto = random.choice(diccionary_phrase[number])
    return esto

# Main execution
if __name__ == "__main__":
    bot_instance = TelegramBot()
    bot_instance.run()