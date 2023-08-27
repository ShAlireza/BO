FROM python:3.9

WORKDIR /app

COPY requirements.txt .

COPY mc /usr/bin/mc

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD export HOST=$(hostname=$(cat /etc/hostname) && grep $hostname /etc/hosts | awk '{print$1}') &&  uvicorn main:app --port 8000 --host 0.0.0.0
