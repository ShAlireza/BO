FROM ubuntu:latest

RUN apt-get update -y && apt-get install -y \
	python3 \
	python3-dev \
	python3-pip \
	git \
	cron \
	&& ln -s /usr/bin/python3 /usr/bin/python \
	&& pip3 install --upgrade pip

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt


COPY . .

EXPOSE 8000

CMD service cron restart && uvicorn main:app --port 8000 --host 0.0.0.0
# CMD ["service", "cron", "start", "&&", "uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
