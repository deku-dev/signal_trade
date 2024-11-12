from telethon import TelegramClient, sync
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

from connection import get_telegram_client

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Параметри для підключення до Telegram API
api_id = os.getenv("TELEGRAM_API_ID")
api_hash = os.getenv("TELEGRAM_API_ID")
phone_number = os.getenv("TELEGRAM_PHONE")

# Параметри для підключення до MySQL
DATABASE_URI = 'mysql+mysqlconnector://your_db_user:your_db_password@localhost/your_db_name'

# Список Telegram-каналів для завантаження повідомлень
channels = ['channel_username_1', 'channel_username_2']  # замініть на ваші канали

# Налаштування SQLAlchemy
engine = create_engine(DATABASE_URI)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

# Модель для таблиці telegram_posts
class TelegramPost(Base):
    __tablename__ = 'telegram_posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    channel_id = Column(BigInteger)
    message_id = Column(BigInteger)
    content = Column(Text)
    is_signal = Column(Boolean, default=False)
    reviewed = Column(Boolean, default=False)
    media_url = Column(String(255))
    timestamp = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    source = Column(String(255))

# Створення таблиці, якщо вона ще не існує
Base.metadata.create_all(engine)

# Підключення до Telegram API
client = get_telegram_client()

# Функція для збереження поста в базу даних
def save_post_to_db(channel_id, message_id, content, media_url, timestamp, source):
    post = TelegramPost(
        channel_id=channel_id,
        message_id=message_id,
        content=content,
        media_url=media_url,
        timestamp=timestamp,
        source=source
    )
    session.add(post)
    session.commit()
    print(f"Збережено повідомлення {message_id} з каналу {source}")

# Основна функція для завантаження постів з каналів
def fetch_and_store_posts():
    for channel in channels:
        # Отримуємо ID каналу
        entity = client.get_entity(channel)
        for message in client.iter_messages(entity, limit=100):  # Встановіть limit для обмеження кількості постів
            content = message.message or ''
            media_url = message.media and message.media.document or None
            timestamp = message.date

            # Збереження повідомлення в базу
            save_post_to_db(
                channel_id=entity.id,
                message_id=message.id,
                content=content,
                media_url=media_url,
                timestamp=timestamp,
                source=channel
            )

# Виклик функцій
fetch_and_store_posts()
client.disconnect()
session.close()
