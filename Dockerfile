# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Define build argument for the token
ARG TELEGRAM_TOKEN
# Set it as environment variable
ENV TELEGRAM_TOKEN=$TELEGRAM_TOKEN

# Run the bot
CMD ["python", "renum_telebot.py"]