FROM docker.arvancloud.ir/python:3.11-slim

WORKDIR /app

RUN apt-get update && \
    apt-get -y install python3-dev default-libmysqlclient-dev pkg-config gcc && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt ./

RUN pip --default-timeout=1000 install -r requirements.txt

COPY . .

ENTRYPOINT ["python3", "-u"]

CMD ["main.py"]
