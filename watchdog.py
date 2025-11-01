import time 
import subprocess
import logging 
import os
from datetime import datetime

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join('logs', 'bot_watchdog.log')),
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
        self.max_restarts = 10  # Maximum consecutive restart attempts
        self.restart_count = 0
        self.base_timeout = 30  # Base timeout in seconds
        self.max_timeout = 3600  # Maximum timeout (1 hour)
        self.last_restart = 0
        self.consecutive_failures = 0
        self.total_restarts = 0

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
                # print("Bot container successfully restarted")
                self.restart_count = 0  # Reset counter on successful start
                self.consecutive_failures = 0  # Reset consecutive failures
                self.total_restarts += 1
                return True
            else:
                logging.error(f"Failed to restart bot container: {result.stderr}")
                # print(f"Failed to restart bot container: {result.stderr}")
                self.consecutive_failures += 1
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

            # logging.info(f"Bot container status: {status}, health: {health}")
            
            # Container should be 'running' and either 'healthy' or no health check
            return status == "running" and (health in ["healthy", "none"])

        except subprocess.CalledProcessError as e:
            logging.error(f"Error checking bot status: {e.stderr}")
            return False
        except Exception as e:
            logging.error(f"Unexpected error checking bot status: {str(e)}")
            return False

    def get_backoff_time(self):
        """Calculate exponential backoff time based on consecutive failures"""
        # Exponential backoff: base_timeout * (2 ^ consecutive_failures)
        # Capped at max_timeout
        backoff = self.base_timeout * (2 ** min(self.consecutive_failures, 5))
        return min(backoff, self.max_timeout)

    def check_and_restart(self):
        """Check bot status and restart if necessary with exponential backoff"""
        if not self.is_bot_running():
            current_time = time.time()
            
            # Calculate backoff time based on consecutive failures
            backoff_time = self.get_backoff_time()
            time_since_last_restart = current_time - self.last_restart
            
            # Check if enough time has passed since last restart attempt
            if self.last_restart > 0 and time_since_last_restart < backoff_time:
                remaining_time = int(backoff_time - time_since_last_restart)
                if remaining_time % 60 == 0 or remaining_time < 10:  # Log every minute or last 10 seconds
                    logging.info(f"Waiting {remaining_time}s before next restart attempt (backoff: {int(backoff_time)}s)")
                return
            
            # UNLIMITED RESTARTS MODE: Check limit disabled
            # Uncomment the following block to re-enable restart limits:
            # if self.consecutive_failures >= self.max_restarts:
            #     logging.error(
            #         f"Bot failed {self.consecutive_failures} consecutive times. "
            #         f"Next retry in {int(backoff_time)}s. Total restarts: {self.total_restarts}"
            #     )
            #     # Wait for backoff time before trying again
            #     time.sleep(backoff_time)
            #     self.consecutive_failures = 0  # Reset after waiting
            
            # Log restart attempt with backoff info
            logging.info(
                f"Bot is down. Restart attempt #{self.consecutive_failures + 1}. "
                f"Total restarts: {self.total_restarts}"
            )
            self.last_restart = current_time
            self.start_bot()

    def run(self):
        """Main watchdog loop"""
        logging.info("Docker Watchdog started")
        # print("Docker Watchdog started")
        
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
                # print(f"Watchdog error: {str(e)}")
                time.sleep(30)  # Wait longer on error

if __name__ == "__main__":
    watchdog = BotWatchdog()
    watchdog.run()