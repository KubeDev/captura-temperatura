FROM python:3.8-slim-buster
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
WORKDIR /app
COPY . /app
RUN useradd appuser && chown -R appuser /app
USER appuser

ENV QUEUE_HOST="localhost"
ENV QUEUE="evento"
ENV ROUTING_KEY="evento"
ENV EXCHANGE=""
ENV RABBITMQ_USER="queueUser"
ENV RABBITMQ_PWD="queuePwd"
ENV MONGODB_DB="admin"
ENV MONGODB_HOST="localhost"
ENV MONGODB_PORT="27017"
ENV MONGODB_USERNAME="mongouser"
ENV MONGODB_PASSWORD="mongopwd"
ENV JAEGER_HOST="localhost"

CMD ["python3", "app.py"]