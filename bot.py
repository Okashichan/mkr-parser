import telebot
from config import TELEGRAM_BOT_TOKEN
from mongo import collection
#from parser_test import get_data_two
from mkrParser import get_week_data, get_weeks_data, get_weeks_data_optimized, get_week_data_optimized

bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)


@bot.message_handler(commands=['start'])
def start_message(message):
    if collection.find_one({'user_id': message.chat.id}):
        print('Already exist')
    else:
        collection.insert_one({
            'user_id': message.chat.id,
            'university_id': '',
            'university_url': '',
            'user_name': message.chat.username,
            'first_name': message.chat.first_name,
            'last_name': message.chat.last_name
            })
        print('Added to database')
    bot.send_message(message.chat.id, 'Для получения документации напишите /help')


@bot.message_handler(commands=['config'])
def config_message(message):
    query = collection.find_one({'user_id': message.chat.id})
    unique_id = query.get('_id')
    university_id = query.get('university_id')
    university_url = query.get('university_url')

    bot.send_message(message.chat.id, f'unique\\_id \\- `{unique_id}`\nuniversity\\_id \\- `{university_id}`\nuniversity\\_url \\- `{university_url}`', parse_mode='MarkdownV2')


@bot.message_handler(commands=['set_university_id'])
def set_university_id(message):
    query = collection.find_one({'user_id': message.chat.id})
    command = message.text.split(' ')
    if len(command) == 1:
        bot.send_message(message.chat.id, 'Укажите ваш ID')
        return
    else:
        university_id = command[1].strip()
        updated_query = { '$set': { 'university_id' : university_id } }
        collection.update_one(query, updated_query)
        print('Updated university_id') 

        bot.send_message(message.chat.id, 'Ваш ID был успешно установлен!')


@bot.message_handler(commands=['set_university_url'])
def set_university_url(message):
    query = collection.find_one({'user_id': message.chat.id})
    command = message.text.split(' ')
    if len(command) == 1:
        bot.send_message(message.chat.id, 'Укажите ваш URL')
        return
    else:
        university_url = command[1].strip()
        updated_query = { '$set': { 'university_url' : university_url } }
        collection.update_one(query, updated_query)
        print('Updated university_url') 

        bot.send_message(message.chat.id, 'Ваш URL был успешно установлен!')


@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, '''Этот бот создан для просмотра расписания в системе МКР
Посмотреть конфигурацию /config
Установить ID /set\\_university\\_id \\<ID\\>
Установить URL /set\\_university\\_url \\<URL\\>
Получить расписание на 5 недель /get\\_weeks
Получить расписание на n\\-ю неделю /get\\_week \\<W1\\-W5\\>
Получить расписание на 5 недель \\(для телефонов\\) /get\\_weeks\\_optimized
Получить расписание на n\\-ю неделю \\(для телефонов\\) /get\\_week\\_optimized \\<W1\\-W5\\>
\nПример правильного конфига:
unique\\_id \\- 61f15ecaf7a2152bc665abe6
university\\_id \\- 99482
university\\_url \\- https://erp\\.kname\\.edu\\.ua/
\nИнструкция по настройке:
/info
\nИнформационный канал по боту: https://t\\.me/mkr\\_news''', parse_mode='MarkdownV2')


@bot.message_handler(commands=['info'])
def info_message(message):
    bot.send_message(message.chat.id, '''Где мне взять URL и ID?
Для этого перейдите на сайт расписания\\. Для примера возьмем "ХДАДМ"\\.
Ссылка на его сайт выглядит следующим образом \\- http://portal\\.ksada\\.org:8090/
Что бы установить URL пишем следующую команду \\- /set\\_university\\_url http://portal\\.ksada\\.org:8090/
\nТеперь перейдем к ID\\. Что бы получить его, переходим по ссылке которую установили\\.
Жмем слева на меню "Расписание", далее выбираем "Студента"\\.
В поле "Поиск студента" пишем свое имя, фамилию и нажимаем на кнопку поиска\\.
Найдите себя в списке который вам выдали, и нажмите "Выбрать"\\.
Тогда в строке браузера у вас появится ссылка следующего вида \\- http://portal\\.ksada\\.org:8090/time\\-table/student?id\\=5598\\.
То что идет после ?id\\= и есть ваш ID\\.
\nЧто бы установить его пишем /set\\_university\\_id 5598\\.
Всё, можно пользоваться ботом\\. /get\\_week
Если данный метод не работает, перейдите в новостоной канал и следуйте инструкции \\#2\\.''', parse_mode='MarkdownV2')


@bot.message_handler(commands=['get_weeks'])
def get_weeks(message):
    query = collection.find_one({'user_id': message.chat.id})
    university_id = query.get('university_id')
    university_url = query.get('university_url')

    if university_id and university_url:
        data = get_weeks_data(id=university_id, url=university_url)
        for d in data:
            d = d.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{d}`', parse_mode='MarkdownV2')
    else: 
        bot.send_message(message.chat.id, 'Для начала укажите ID и URL. Как это сделать? /info')
    print('get_weeks executed by:', query.get('user_name'))


@bot.message_handler(commands=['get_weeks_optimized'])
def get_weeks_optimized(message):
    query = collection.find_one({'user_id': message.chat.id})
    university_id = query.get('university_id')
    university_url = query.get('university_url')

    if university_id and university_url:
        dt1, dt2 = get_weeks_data_optimized(id=university_id, url=university_url)
        for d1, d2 in zip(dt1,dt2):
            d1 = d1.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            d2 = d2.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{d1}`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, f'`{d2}`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, '`----------------------------------`', parse_mode='MarkdownV2')
    else: 
        bot.send_message(message.chat.id, 'Для начала укажите ID и URL. Как это сделать? /info')
    print('get_weeks executed by:', query.get('user_name'))


@bot.message_handler(commands=['get_week'])
def get_week(message):
    query = collection.find_one({'user_id': message.chat.id})
    university_id = query.get('university_id')
    university_url = query.get('university_url')

    if university_id and university_url:
        command = message.text.split(' ')
        if len(command) == 1:
            data = get_week_data(id=university_id, url=university_url)
            data = data.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{data}`', parse_mode='MarkdownV2')
        else:
            data = get_week_data(id=university_id, url=university_url, week=command[1].strip())
            data = data.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{data}`', parse_mode='MarkdownV2')
    else: 
        bot.send_message(message.chat.id, 'Для начала укажите ID и URL. Как это сделать? /info')

    print('get_weeks executed by:', query.get('user_name'))


@bot.message_handler(commands=['get_week_optimized'])
def get_week_optimized(message):
    query = collection.find_one({'user_id': message.chat.id})
    university_id = query.get('university_id')
    university_url = query.get('university_url')

    if university_id and university_url:
        command = message.text.split(' ')
        if len(command) == 1:
            d1, d2 = get_week_data_optimized(id=university_id, url=university_url)
            d1 = d1.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            d2 = d2.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{d1}`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, '`----------------------------------`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, f'`{d2}`', parse_mode='MarkdownV2')
        else:
            d1, d2 = get_week_data_optimized(id=university_id, url=university_url, week=command[1].strip())
            d1 = d1.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            d2 = d2.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")
            bot.send_message(message.chat.id, f'`{d1}`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, '`----------------------------------`', parse_mode='MarkdownV2')
            bot.send_message(message.chat.id, f'`{d2}`', parse_mode='MarkdownV2')
    else: 
        bot.send_message(message.chat.id, 'Для начала укажите ID и URL. Как это сделать? /info')

    print('get_weeks executed by:', query.get('user_name'))


'''
@bot.message_handler(commands=['get_raw_data'])
def get_raw_data_message(message):
    query = collection.find_one({'user_id': message.chat.id})
    university_id = query.get('university_id')
    university_url = query.get('university_url')
    
    if university_id and university_url:
        data = get_data_two(id=university_id, url=university_url)
        if len(data) >= 4096:
            chunks, chunk_size = len(data), len(data) // 2
            data = [ data[i:i+chunk_size] for i in range(0, chunks, chunk_size) ]
            for d in data[:-1]:
                bot.send_message(message.chat.id, d.strip().replace('&nbsp', ''))
        else:
            bot.send_message(message.chat.id, data.strip().replace('&nbsp', ''))
        print('get_raw_data executed by:', query.get('user_name'))
    else:
        bot.send_message(message.chat.id, 'Что бы использовать эту команду установите ваш ID')
'''