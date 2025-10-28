# bot-chad-hue-one
Bot de telegram basado

# Only bot
## Build the image (mandatory after every change)
docker build -t telegram-bot .

## Run the container with your token (optional)
docker run -d -e TELEGRAM_TOKEN="your_token_here" telegram-bot

# Bot and watchdog (Recommended)
## Build and start the services
docker-compose up --build

## Or in detached mode (optional)
docker-compose up -d --build
