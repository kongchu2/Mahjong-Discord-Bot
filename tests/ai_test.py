from types import SimpleNamespace

from src.cmds.ai.command import should_answer
from src.cmds.ai.limiter import DAY_SECONDS, AIRateLimiter
from src.cmds.ai.service import MAX_PROMPT_CHARS, clean_prompt
from src.core.config import Config

BOT = SimpleNamespace(id=1000)
HUMAN = SimpleNamespace(id=1, bot=False)


def message(author=HUMAN, mentions=(BOT,), guild_id=None, system=False):
    return SimpleNamespace(
        author=author,
        mentions=list(mentions),
        guild=SimpleNamespace(id=guild_id) if guild_id is not None else None,
        is_system=lambda: system,
    )


class Clock:
    def __init__(self):
        self.now = 0.0

    def __call__(self):
        return self.now


def test_answers_a_direct_mention():
    assert should_answer(BOT, message(), frozenset())


def test_ignores_messages_from_bots_including_itself():
    assert not should_answer(BOT, message(author=SimpleNamespace(id=BOT.id, bot=True)), frozenset())
    assert not should_answer(BOT, message(author=SimpleNamespace(id=2, bot=True)), frozenset())


def test_ignores_everyone_and_role_pings_without_a_direct_mention():
    assert not should_answer(BOT, message(mentions=()), frozenset())


def test_ignores_system_messages():
    assert not should_answer(BOT, message(system=True), frozenset())


def test_guild_allowlist():
    allowed = frozenset({42})
    assert should_answer(BOT, message(guild_id=42), allowed)
    assert not should_answer(BOT, message(guild_id=7), allowed)
    assert not should_answer(BOT, message(guild_id=None), allowed)  # DM


def test_user_cooldown():
    clock = Clock()
    limiter = AIRateLimiter(user_cooldown=10, daily_limit=0, clock=clock)
    assert limiter.acquire(1) is None
    clock.now = 9
    denied = limiter.acquire(1)
    assert denied is not None and denied.reason == "cooldown"
    assert limiter.acquire(2) is None  # 다른 사용자는 영향 없음
    clock.now = 10
    assert limiter.acquire(1) is None


def test_denied_calls_do_not_extend_the_cooldown():
    clock = Clock()
    limiter = AIRateLimiter(user_cooldown=10, daily_limit=0, clock=clock)
    limiter.acquire(1)
    clock.now = 5
    limiter.acquire(1)
    clock.now = 10
    assert limiter.acquire(1) is None


def test_daily_limit_is_shared_and_rolls_over():
    clock = Clock()
    limiter = AIRateLimiter(user_cooldown=0, daily_limit=2, clock=clock)
    assert limiter.acquire(1) is None
    assert limiter.acquire(2) is None
    denied = limiter.acquire(3)
    assert denied is not None and denied.reason == "daily"
    clock.now = DAY_SECONDS
    assert limiter.acquire(3) is None


def test_clean_prompt_strips_the_bot_mention_and_caps_length():
    assert clean_prompt("<@1000> 안녕 <@!1000>", 1000) == "안녕"
    assert clean_prompt("<@999> hi", 1000) == "<@999> hi"
    assert len(clean_prompt("<@1000> " + "가" * 5000, 1000)) == MAX_PROMPT_CHARS


def test_config_never_describes_secret_values(monkeypatch):
    monkeypatch.setattr(Config, "DISCORD_BOT_TOKEN", "discord-secret")
    monkeypatch.setattr(Config, "OPENAI_APIKEY", None)
    described = Config.describe()
    assert described["DISCORD_BOT_TOKEN"] == "(set)"
    assert described["OPENAI_APIKEY"] == "(not set)"
    assert "discord-secret" not in repr(described)
