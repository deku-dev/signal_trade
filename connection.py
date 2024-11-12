# telegram_client.py
from telethon import TelegramClient
import os

from dotenv import load_dotenv

load_dotenv()

# Параметри для підключення до Telegram API (замініть значення на свої)
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_HASH")
session_name = "SignalTradingBot"

# Ініціалізація клієнта Telethon
client = TelegramClient(session_name, api_id, api_hash)

def get_telegram_client():
    if not client.is_connected():
        client.connect()
    return client
