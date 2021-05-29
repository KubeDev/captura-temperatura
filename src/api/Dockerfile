FROM python:3.8-slim-buster
EXPOSE 5000
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

ENV QUEUE_HOST="localhost"
ENV QUEUE="evento"
ENV ROUTING_KEY="evento"
ENV EXCHANGE=""
ENV RABBITMQ_USER="queueUser"
ENV RABBITMQ_PWD="queuePwd"
ENV JAEGER_HOST="localhost"

WORKDIR /app
COPY . /app
RUN useradd appuser && chown -R appuser /app
USER appuser

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]