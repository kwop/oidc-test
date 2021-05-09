FROM python:3.9.5-buster

WORKDIR /usr/src/app
COPY . /usr/src/app/

RUN [ ! -f client_secrets.json ] && cp client_secrets.json.dist client_secrets.json || echo "client_secrets already setted"

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
CMD python main.py
