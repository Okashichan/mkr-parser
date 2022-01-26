# mkr-parser
Telegram bot for parsing schedule from mkr-websites

## To simply run this bot you need:
```sh
git clone https://github.com/Okashichan/mkr-parser
cd mkr-parser
cp config.py.example config.py # change config strings to yours
pip install -r requirements.txt
python main.py
```

## To deploy as docker container:
```sh
git clone https://github.com/Okashichan/mkr-parser
cd mkr-parser
cp config.py.example config.py # change config strings to yours
docker-compose up -d # to setup mongo database if you dont have one already
docker build -t mkr .
docker run -d --name mkr_bot mkr
```
