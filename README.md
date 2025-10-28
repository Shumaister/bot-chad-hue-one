# bot-chad-hue-one
Bot de telegram basado

# Only bot
## Build the image (mandatory after every change)
docker build -t telegram-bot .

# Bot and watchdog
## Build and start the services (Recommended)
docker-compose up --build

## Or in detached mode (optional)
docker-compose up -d --build
