import re

import openai

from src.core.config import Config

# 한 번에 보내는 질문 길이(비용 상한)와 디스코드 메시지 길이 제한.
MAX_PROMPT_CHARS = 2000
DISCORD_MESSAGE_LIMIT = 2000

# 동기 클라이언트는 응답을 기다리는 동안 이벤트 루프를 막아 봇 전체가 멈추므로 비동기 클라이언트를 씁니다.
_client = (
    openai.AsyncOpenAI(api_key=Config.OPENAI_APIKEY, timeout=30, max_retries=1)
    if Config.OPENAI_APIKEY
    else None
)


def clean_prompt(content: str, bot_id: int) -> str:
    """봇 멘션을 지우고 길이를 제한합니다. 멘션이 남으면 모델이 따라 써서 봇이 자기 자신을 다시 부를 수 있습니다."""
    text = re.sub(rf"<@!?{bot_id}>", "", content).strip()
    return text[:MAX_PROMPT_CHARS]


async def prompt(text: str) -> str:
    if _client is None:
        return "비활성화된 기능입니다."
    if not text:
        return "질문을 함께 적어 주세요."
    try:
        completion = await _client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": text},
            ],
            temperature=0.7,
            max_tokens=500,
        )

        answer = completion.choices[0].message.content or ""
        return answer[:DISCORD_MESSAGE_LIMIT] or "응답이 비어 있습니다."
    except Exception as e:
        print(e)
        return "응답에 실패했습니다."
