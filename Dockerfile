FROM python:3.8

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY app/ ./app
COPY model/ ./model

CMD ["python", "app/main.py"]