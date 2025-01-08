FROM python:3.10-slim

WORKDIR /src

COPY . /src
COPY ./main.py /main.py

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "main.py"]
