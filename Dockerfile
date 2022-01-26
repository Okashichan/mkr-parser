FROM python:slim

WORKDIR /coursework-app

COPY . .

RUN pip install -r requirements.txt

CMD [ "python", "./main.py" ]