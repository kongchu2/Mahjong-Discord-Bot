import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass
from typing import Literal

DAY_SECONDS = 24 * 60 * 60


@dataclass(frozen=True)
class Denied:
    reason: Literal["cooldown", "daily"]
    retry_after: float


class AIRateLimiter:
    """사용자별 쿨다운과 봇 전체의 24시간 호출 상한. 메모리에만 두므로 재시작하면 초기화됩니다."""

    def __init__(
        self,
        user_cooldown: float,
        daily_limit: int,
        clock: Callable[[], float] = time.monotonic,
    ):
        self._user_cooldown = user_cooldown
        self._daily_limit = daily_limit
        self._clock = clock
        self._last_call: dict[int, float] = {}
        self._recent_calls: deque[float] = deque()

    def acquire(self, user_id: int) -> Denied | None:
        """허용되면 호출을 기록하고 None을, 아니면 거절 사유를 돌려줍니다."""
        now = self._clock()

        if self._user_cooldown > 0:
            last = self._last_call.get(user_id)
            if last is not None and now - last < self._user_cooldown:
                return Denied("cooldown", self._user_cooldown - (now - last))

        if self._daily_limit > 0:
            while self._recent_calls and now - self._recent_calls[0] >= DAY_SECONDS:
                self._recent_calls.popleft()
            if len(self._recent_calls) >= self._daily_limit:
                return Denied("daily", DAY_SECONDS - (now - self._recent_calls[0]))
            self._recent_calls.append(now)

        self._last_call[user_id] = now
        return None
