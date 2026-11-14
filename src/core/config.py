# config.py
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")


def _env_float(name: str, default: float) -> float:
    value = os.getenv(name)
    return float(value) if value else default


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    return int(value) if value else default


def _env_ids(name: str) -> frozenset[int]:
    value = os.getenv(name, "")
    return frozenset(int(part) for part in value.split(",") if part.strip())


# 값을 로그에 남기면 안 되는 항목. print_config는 설정 여부만 출력합니다.
_SECRET_KEYS = frozenset({"DISCORD_BOT_TOKEN", "OPENAI_APIKEY"})


class Config:
    DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
    MAHJONG_IMAGE_FOLDER_PATH = os.getenv("MAHJONG_IMAGE_FOLDER_PATH", "image/mahjong")
    SUTDA_IMAGE_FOLDER_PATH = os.getenv("SUTDA_IMAGE_FOLDER_PATH", "image/hwatu")
    OPENAI_APIKEY = os.getenv("OPENAI_APIKEY")

    # AI(멘션) 응답 한도. 0이면 해당 제한을 끕니다.
    AI_USER_COOLDOWN_SECONDS = _env_float("AI_USER_COOLDOWN_SECONDS", 10)
    AI_DAILY_LIMIT = _env_int("AI_DAILY_LIMIT", 200)
    # 쉼표로 구분한 서버(guild) ID. 비워 두면 모든 서버에서 응답하고, 설정하면 그 서버에서만 응답합니다(DM 제외).
    AI_ALLOWED_GUILD_IDS = _env_ids("AI_ALLOWED_GUILD_IDS")

    @staticmethod
    def print_config():
        for key, value in Config.describe().items():
            print(f"{key}: {value}")

    @staticmethod
    def describe() -> dict[str, object]:
        """설정값을 로그에 남겨도 되는 형태로 돌려줍니다. 비밀 값은 설정 여부만 보여 줍니다."""
        described: dict[str, object] = {}
        for key, value in vars(Config).items():
            if not key.isupper():
                continue
            if key in _SECRET_KEYS:
                value = "(set)" if value else "(not set)"
            described[key] = value
        return described
