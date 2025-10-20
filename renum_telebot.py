import os
import time
from dotenv import load_dotenv
import telebot
import logging
import random
from telebot.handler_backends import State, StatesGroup

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'renum_telebot.log')),
        logging.StreamHandler()
    ]
)

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
        logging.info("Arriba Bot... boiung bouign ,biip pipi bippo ya estoy andando")
    
    def setup_handlers(self):
        @self.bot.message_handler(content_types=['new_chat_members'])
        def welcome_new_members(message):
            try:
                for new_member in message.new_chat_members:
                    if new_member.id == self.bot.get_me().id:
                        self.bot.reply_to(message, "¡Hola! Me han agregado al grupo. Estaré leyendo los mensajes 👀")
            except Exception as e:
                print(f"Error en welcome_new_members: {str(e)}")
                logging.error(f"Error en welcome_new_members: {str(e)}")
        
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

                # Check if the message ends with a number
                last_word = text.split()[-1]
                if last_word in ["4", "13"]:
                    self.bot.reply_to(message, self.lookup_random_phrases(last_word))
                    return
                if last_word in {"5", "8", "9", "11", "12"}:
                    self.bot.reply_to(message, self.lookup_simple_phrases(last_word))
                    return
                
                # Check if message contains specific word
                if "fabio" in text or "Fabio" in text:
                    self.bot.reply_to(message, "Es con V corta irrespetuoso de mierda. Ta bien que es oscuro pero pará...")
                    return
                
                # Check if it's a greeting
                if text.lower() in ["hola", "hello", "hi"]:
                    self.bot.reply_to(message, f"Tu nariz contra mis bolas. Ahora si, Hola {user_name}! ¿En qué te puedo ayudar?")
                    return               
                                                    
            except Exception as e:
                print(f"Exception processing mesage: Message: {message.text} - Ex: {str(e)}")
                logging.error(f"Exception processing mesage: Message: {message.text} - Ex: {str(e)}")

    def run(self):
        while True:
            try:
                print("Bot listo y escuchando mensajes...")
                logging.info("Bot listo y escuchando mensajes...")
                self.bot.polling(non_stop=True, interval=2)
            except Exception as e:
                print(f"Error crítico del bot: {str(e)}")
                print("Reintentando en 10 segundos...")
                logging.error(f"Error crítico del bot: {str(e)}")
                time.sleep(10)
                self.setup_bot()  # Recreate bot instance
                
    def lookup_random_phrases(self, number):
        diccionary_phrase = { 
            "4":    ["El culo te parto", "Te puse", "La ponen", "Alla", "Te puse"],
            "13":   ["Mas me la mamas mas me crece", "Agarra LA que me crece", "while true: me crece"]
        }   
        return random.choice(diccionary_phrase[number])
    
    def lookup_simple_phrases(self, number):
        return {
                    "5": "POR EL CULO TE LA HINCO",
                    "8": "EL CULO TE ABROCHO",
                    "9": "EL CULO TE LLUEVE",
                    "12": "SI TE ROMPO EL CULO QUIEN TE LO COSE",
                    "11": "CHUPALO ENTONCE"
                }[number]

# Main execution
if __name__ == "__main__":
    bot_instance = TelegramBot()
    bot_instance.run()
