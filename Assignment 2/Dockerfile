# syntax=docker/dockerfile:1
FROM python:3.12-slim

COPY requirements.txt /src/requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /src/requirements.txt

WORKDIR /app/

COPY . .

EXPOSE 8080

CMD [ "python", "/app/manage.py", "runserver" ]
