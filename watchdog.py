import time 
import subprocess
import logging 
from datetime import datetime
 
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot_watchdog.log'),
        logging.StreamHandler()
    ]
)

# Configure Docker-specific settings
BOT_HOST = 'bot'  # Docker service name
BOT_PORT = 8443   # Telegram bot port

class BotWatchdog:
    def __init__(self):
        self.bot_script = "renum_telebot.py"
        self.bot_process = None
        self.max_restarts = 5
        self.restart_count = 0
        self.restart_timeout = 30  # 5 minutes between restart attempts
        self.last_restart = 0

    def start_bot(self):
        """Restart the bot container using Docker"""
        try:
            # Stop the bot container if it's running
            subprocess.run(
                ["docker", "stop", "telegram-bot"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=False  # Don't raise exception if container is not running
            )

            # Start the bot container
            result = subprocess.run(
                ["docker", "start", "telegram-bot"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            if result.returncode == 0:
                logging.info("Bot container successfully restarted")
                print("Bot container successfully restarted")
                self.restart_count = 0  # Reset counter on successful start
                return True
            else:
                logging.error(f"Failed to restart bot container: {result.stderr}")
                print(f"Failed to restart bot container: {result.stderr}")
                return False

        except subprocess.CalledProcessError as e:
            logging.error(f"Docker command failed: {e.stderr}")
            #print(f"Docker command failed: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"Failed to restart bot: {str(e)}")
            #print(f"Failed to restart bot: {str(e)}")
            return False

    def is_bot_running(self):
        """Check if the bot container is running and healthy"""
        try:
            # Check container status using docker inspect
            result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Status}}", "telegram-bot"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            
            # Get container health if available
            health_result = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Health.Status}}", "telegram-bot"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=False
            )

            status = result.stdout.strip()
            health = health_result.stdout.strip() if health_result.returncode == 0 else "none"

            logging.info(f"Bot container status: {status}, health: {health}")
            
            # Container should be 'running' and either 'healthy' or no health check
            return status == "running" and (health in ["healthy", "none"])

        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking bot status: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error checking bot status: {str(e)}")
            return False

    def check_and_restart(self):
        """Check bot status and restart if necessary"""
        if not self.is_bot_running():
            current_time = time.time()
            
            # Check if we've exceeded max restarts within timeout period
            if current_time - self.last_restart < self.restart_timeout:
                self.restart_count += 1
                if self.restart_count >= self.max_restarts:
                    logging.error(f"Bot failed to start {self.max_restarts} times in {self.restart_timeout} seconds. Waiting...")
                    print(f"Bot failed to start {self.max_restarts} times in {self.restart_timeout} seconds. Waiting...")
                    time.sleep(self.restart_timeout)
                    self.restart_count = 0
            else:
                self.restart_count = 0

            logging.info("Bot is down, attempting to restart...")
            #print("Bot is down, attempting to restart...")
            self.last_restart = current_time
            self.start_bot()

    def run(self):
        """Main watchdog loop"""
        logging.info("Docker Watchdog started")
        print("Docker Watchdog started")
        
        while True:
            try:
                self.check_and_restart()
                
                # Get container logs for the last 10 seconds
                log_result = subprocess.run(
                    ["docker", "logs", "--since", "10s", "telegram-bot"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    check=False
                )
                
                if log_result.stdout:
                    print(f"Bot logs: {log_result.stdout.strip()}")
                
                time.sleep(10)  # Check every 10 seconds
                
            except Exception as e:
                logging.error(f"Watchdog error: {str(e)}")
                print(f"Watchdog error: {str(e)}")
                time.sleep(30)  # Wait longer on error

if __name__ == "__main__":
    watchdog = BotWatchdog()
    watchdog.run()