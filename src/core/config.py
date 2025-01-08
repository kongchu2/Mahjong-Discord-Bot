# config.py
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


class Config:
    DISCORD_BOT_TOKEN = os.getenv("TOKEN")
    MAHJONG_IMAGE_FOLDER_PATH = os.getenv("MAHJONG_IMAGE_FOLDER_PATH", "image/mahjong")
    SUTDA_IMAGE_FOLDER_PATH = os.getenv("SUTDA_IMAGE_FOLDER_PATH", "image/hwatu")

    @staticmethod
    def print_config():
        for key, value in Config.__dict__.items():
            if not key.startswith("__") and key != "print_config":
                print(f"{key}: {value}")
