# Huge help by https://stackoverflow.com/users/15568504/simpleapp
# Solution https://stackoverflow.com/questions/70856448/python-bs4-lxml-parsing-table
import pandas as pd
from io import BytesIO
from selenium import webdriver
from selenium.webdriver import FirefoxOptions
from webdriver_manager.firefox import GeckoDriverManager


opts = FirefoxOptions()
opts.add_argument("--headless")

df_header = [ 'Day', 'W1', 'W2', 'W3', 'W4', 'W5' ]
search = 'time-table/student?id='


def parse(url, id, search=search):

    table_list=pd.read_html(url+search+id, attrs = {'id': 'timeTable'}, flavor='lxml')

    df = table_list[0].replace(r'&nbsp','Нет пары', regex=True) # replace the value with NoValue, in case needed further
    df.columns=df_header # logical header 

    #converting header to first row data
    df_t=pd.DataFrame(columns=df_header, data=[table_list[0].columns.tolist()])
    df_final=df_t.append(df, ignore_index=True)

    #setup for group weeks
    week_days_notation=['Пн','Вт','Ср','Чт','Пт','Сб','Нд']
    day_of_week=""
    week_days=[]
    for e in df_final['Day']:
        if e in week_days_notation:
            day_of_week=e
        week_days.append(day_of_week)
    #week_days

    # add the week_days to the dataframe
    df_final.insert(0,'week_group', week_days)

    return df_final


def get_weeks_data(url, id):

    df_final = parse(url, id)

    for e, w in zip(df_final, df_header):
        df_final.loc[:,[w]] = df_final.loc[:,[w]].replace(r'[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}', '', regex=True)

    return df_final.loc[:,['Day', 'W1']].to_markdown(index=False),  df_final.loc[:,['Day', 'W2']].to_markdown(index=False),  df_final.loc[:,['Day', 'W3']].to_markdown(index=False),  df_final.loc[:,['Day', 'W4']].to_markdown(index=False),  df_final.loc[:,['Day', 'W5']].to_markdown(index=False)


def get_weeks_data_optimized(url, id):

    df_final = parse(url, id)
    
    return [[df_final.loc[:,['Day']].to_markdown(index=False),  df_final.loc[:,['Day']].to_markdown(index=False),  df_final.loc[:,['Day']].to_markdown(index=False),  df_final.loc[:,['Day']].to_markdown(index=False),  df_final.loc[:,['Day']].to_markdown(index=False)],
            [df_final.loc[:,['W1']].to_markdown(index=False),  df_final.loc[:,['W2']].to_markdown(index=False),  df_final.loc[:,['W3']].to_markdown(index=False),  df_final.loc[:,['W4']].to_markdown(index=False),  df_final.loc[:,['W5']].to_markdown(index=False)]]


def get_week_data(url, id, week='W1'):

    df_final = parse(url, id)

    df_final.loc[:,[week]] = df_final.loc[:,[week]].replace(r'[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}', '', regex=True)
    
    return df_final.loc[:,['Day', week]].to_markdown(index=False)


def get_week_data_optimized(url, id, week='W1'):

    df_final = parse(url, id)

    df_final.loc[:,[week]] = df_final.loc[:,[week]].replace(r'[0-9]{2}:[0-9]{2}-[0-9]{2}:[0-9]{2}', '', regex=True)

    return [df_final.loc[:,['Day']].to_markdown(index=False),df_final.loc[:,[week]].to_markdown(index=False)]


def get_weeks_data_img(url, id, search=search):
    fox = webdriver.Firefox(executable_path=GeckoDriverManager().install(), options=opts)

    try:
        fox.get(url+search+id)
        image = BytesIO(fox.find_element_by_tag_name('table').screenshot_as_png)
        image.name = id + '.png'
    except:
        fox.close()

    fox.close()

    return image

#get_weeks_data_img('http://portal.ksada.org:8090/', '5598')