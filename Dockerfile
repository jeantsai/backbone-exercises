FROM smebberson/alpine-consul-base:4.1.0

WORKDIR /app

COPY requirements.txt ./
#COPY backend.py ./

RUN apk upgrade --update --no-cache && \
    apk add --update --no-cache python3 && \
    rm -rf /var/cache/apk/* && \
    pip3 install --no-cache-dir --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    pip install --no-cache-dir -r requirements.txt
