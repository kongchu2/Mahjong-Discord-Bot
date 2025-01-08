import openai

from src.core.config import Config

openai.api_key = Config.OPENAI_APIKEY


def prompt(prompt) -> str:
    if Config.OPENAI_APIKEY is None:
        return "비활성화된 기능입니다."
    try:
        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
            max_tokens=150,
        )

        return str(completion.choices[0].message.content)
    except Exception as e:
        print(e)
        return "응답에 실패했습니다."
