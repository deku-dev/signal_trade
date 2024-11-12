from telethon import TelegramClient, sync
from sqlalchemy import create_engine, Column, Integer, BigInteger, Text, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from connection import get_telegram_client
import os

from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.