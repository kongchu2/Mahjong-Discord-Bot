FROM python:3.12-slim

WORKDIR /src

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 실행에 필요한 파일만 복사합니다. .env는 docker compose의 env_file로 주입되므로 이미지에 넣지 않습니다.
COPY main.py .
COPY src ./src
COPY image ./image

RUN useradd --create-home --uid 10001 bot
USER bot

CMD ["python", "main.py"]
