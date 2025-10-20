# bot-chad-hue-one
Bot de telegram basado

# Only bot
## Build the image
docker build -t telegram-bot .

## Run the container with your token
docker run -d -e TELEGRAM_TOKEN="your_token_here" telegram-bot

# Bot and watchdog
## Build and start the services
docker-compose up --build

## Or in detached mode
docker-compose up -d --build
