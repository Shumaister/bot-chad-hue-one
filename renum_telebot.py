import os
import time
from dotenv import load_dotenv
import telebot
import logging
import random
import json
from datetime import datetime
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
        self.strikes_file = 'strikes_data.json'
        self.strikes_data = self.load_strikes()
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
    
    def load_strikes(self):
        """Carga los datos de strikes desde el archivo JSON"""
        try:
            if os.path.exists(self.strikes_file):
                with open(self.strikes_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logging.error(f"Error cargando strikes: {str(e)}")
            return {}
    
    def save_strikes(self):
        """Guarda los datos de strikes en el archivo JSON"""
        try:
            with open(self.strikes_file, 'w', encoding='utf-8') as f:
                json.dump(self.strikes_data, f, ensure_ascii=False, indent=2)
            logging.info("Strikes guardados exitosamente")
        except Exception as e:
            logging.error(f"Error guardando strikes: {str(e)}")
    
    def add_strike(self, user_id, username, reason, requested_by, requested_by_username):
        """Agrega un strike a un usuario"""
        user_key = str(user_id)
        
        if user_key not in self.strikes_data:
            self.strikes_data[user_key] = {
                'username': username,
                'strikes': []
            }
        
        strike = {
            'reason': reason,
            'requested_by': requested_by,
            'requested_by_username': requested_by_username,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        self.strikes_data[user_key]['strikes'].append(strike)
        self.strikes_data[user_key]['username'] = username  # Actualizar username por si cambió
        self.save_strikes()
        
        return len(self.strikes_data[user_key]['strikes'])
    
    def remove_strike(self, user_id):
        """Remueve el último strike de un usuario"""
        user_key = str(user_id)
        
        if user_key in self.strikes_data and self.strikes_data[user_key]['strikes']:
            removed_strike = self.strikes_data[user_key]['strikes'].pop()
            self.save_strikes()
            return True, removed_strike
        
        return False, None
    
    def get_strikes(self, user_id):
        """Obtiene los strikes de un usuario"""
        user_key = str(user_id)
        
        if user_key in self.strikes_data:
            return self.strikes_data[user_key]['strikes']
        
        return []
    
    def get_user_from_message(self, message, text):
        """Extrae el usuario mencionado del mensaje"""
        # Verificar si hay un usuario mencionado mediante reply
        if message.reply_to_message:
            return message.reply_to_message.from_user
        
        # Verificar si hay un @ en el texto
        words = text.split()
        for word in words:
            if word.startswith('@'):
                # Buscar en las entidades del mensaje
                if message.entities:
                    for entity in message.entities:
                        if entity.type == 'mention':
                            username = word[1:]  # Remover @
                            # No podemos obtener el ID solo con el username, necesitamos que sea un reply o text_mention
                            return None, username
                        elif entity.type == 'text_mention':
                            return entity.user
        
        return None

    
    def setup_handlers(self):
        @self.bot.message_handler(commands=['renum_strikeadd'])
        def handle_strike_add(message):
            try:
                # Verificar si es un grupo
                if message.chat.type not in ['group', 'supergroup']:
                    self.bot.reply_to(message, "Este comando solo funciona en grupos.")
                    return
                
                text = message.text
                parts = text.split(maxsplit=1)
                
                # Obtener el usuario objetivo
                target_user = None
                reason = ""
                
                # Caso 1: Responder a un mensaje (MÉTODO RECOMENDADO)
                if message.reply_to_message:
                    target_user = message.reply_to_message.from_user
                    if len(parts) >= 2:
                        reason = parts[1]
                    else:
                        self.bot.reply_to(message, 
                            "❌ Debes proporcionar un motivo para el strike.\n"
                            "Ejemplo: /renum_strikeadd Spam en el grupo")
                        return
                
                # Caso 2: Sin reply - mostrar instrucciones
                else:
                    self.bot.reply_to(message, 
                        "❌ Debes responder al mensaje del usuario al que quieres agregar un strike.\n\n"
                        "📝 Instrucciones:\n"
                        "1. Responde al mensaje del usuario\n"
                        "2. Escribe: /renum_strikeadd [motivo]\n\n"
                        "Ejemplo:\n"
                        "[Responde a un mensaje]\n"
                        "/renum_strikeadd Spam en el grupo")
                    return
                
                if not reason.strip():
                    self.bot.reply_to(message, "❌ Debes proporcionar un motivo para el strike.")
                    return
                
                # Agregar el strike
                requester = message.from_user
                total_strikes = self.add_strike(
                    target_user.id,
                    target_user.username or target_user.first_name,
                    reason,
                    requester.id,
                    requester.username or requester.first_name
                )
                
                response = (
                    f"⚠️ Strike agregado a {target_user.first_name}\n"
                    f"📝 Motivo: {reason}\n"
                    f"👮 Solicitado por: {requester.first_name}\n"
                    f"📊 Total de strikes: {total_strikes}"
                )
                
                self.bot.reply_to(message, response)
                logging.info(f"Strike agregado a {target_user.id} por {requester.id}: {reason}")
                
            except Exception as e:
                logging.error(f"Error en handle_strike_add: {str(e)}")
                self.bot.reply_to(message, f"Error al agregar strike: {str(e)}")
        
        @self.bot.message_handler(commands=['renum_strikerem'])
        def handle_strike_remove(message):
            try:
                # Verificar si es un grupo
                if message.chat.type not in ['group', 'supergroup']:
                    self.bot.reply_to(message, "Este comando solo funciona en grupos.")
                    return
                
                # Obtener el usuario objetivo
                target_user = None
                
                # Caso 1: Responder a un mensaje (MÉTODO RECOMENDADO)
                if message.reply_to_message:
                    target_user = message.reply_to_message.from_user
                
                # Caso 2: Sin reply - mostrar instrucciones
                else:
                    self.bot.reply_to(message, 
                        "❌ Debes responder al mensaje del usuario al que quieres remover un strike.\n\n"
                        "📝 Instrucciones:\n"
                        "1. Responde al mensaje del usuario\n"
                        "2. Escribe: /renum_strikerem\n\n"
                        "Esto removerá el último strike agregado.")
                    return
                
                # Remover el strike
                success, removed_strike = self.remove_strike(target_user.id)
                
                if success:
                    remaining_strikes = len(self.get_strikes(target_user.id))
                    response = (
                        f"✅ Strike removido de {target_user.first_name}\n"
                        f"📊 Strikes restantes: {remaining_strikes}"
                    )
                    if removed_strike:
                        response += f"\n📝 Strike removido: {removed_strike['reason']}"
                else:
                    response = f"❌ {target_user.first_name} no tiene strikes para remover."
                
                self.bot.reply_to(message, response)
                logging.info(f"Strike removido de {target_user.id}")
                
            except Exception as e:
                logging.error(f"Error en handle_strike_remove: {str(e)}")
                self.bot.reply_to(message, f"Error al remover strike: {str(e)}")
        
        @self.bot.message_handler(commands=['renum_strikecheck'])
        def handle_strike_check(message):
            try:
                # Obtener el usuario objetivo
                target_user = None
                
                # Caso 1: Responder a un mensaje
                if message.reply_to_message:
                    target_user = message.reply_to_message.from_user
                
                # Caso 2: Consultar strikes propios
                else:
                    target_user = message.from_user
                
                # Obtener strikes
                strikes = self.get_strikes(target_user.id)
                
                if not strikes:
                    self.bot.reply_to(message, f"✅ {target_user.first_name} no tiene strikes.")
                    return
                
                response = f"📋 Strikes de {target_user.first_name} ({len(strikes)} total):\n\n"
                
                for i, strike in enumerate(strikes, 1):
                    response += (
                        f"{i}. 📝 {strike['reason']}\n"
                        f"   👮 Por: {strike['requested_by_username']}\n"
                        f"   📅 Fecha: {strike['date']}\n\n"
                    )
                
                self.bot.reply_to(message, response)
                
            except Exception as e:
                logging.error(f"Error en handle_strike_check: {str(e)}")
                self.bot.reply_to(message, f"Error al consultar strikes: {str(e)}")
        
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
                    if command in ['/renum-start', '/renum-help', '/renum_help']:
                        self.bot.reply_to(
                            message,
                            f"""Hola {user_name}, soy tu bot.
                            {group_info}
                            
                            📋 Comandos de Strikes:
                            • /renum_strikeadd - Agregar strike (responde al mensaje del usuario)
                            • /renum_strikerem - Remover strike (responde al mensaje del usuario)
                            • /renum_strikecheck - Ver tus strikes o de otro usuario
                            
                            💡 Cómo usar:
                            1. Responde al mensaje del usuario
                            2. Escribe el comando
                            
                            Otras funciones:
                            • Responder a saludos
                            • Dar respuestas especiales a números y palabras clave""")
                    else:
                        self.bot.reply_to(message, f"Comando {command} no reconocido. Usa /renum_help para ver los comandos disponibles.")
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
