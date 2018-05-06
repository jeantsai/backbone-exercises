FROM python:alpine

WORKDIR /app

COPY requirements.txt ./
#COPY backend.py ./

RUN pip install --no-cache-dir -r requirements.txt
