FROM python:slim

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install firefox-esr -y
RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]