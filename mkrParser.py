# Huge help by https://stackoverflow.com/users/15568504/simpleapp
# Solution https://stackoverflow.com/questions/70856448/python-bs4-lxml-parsing-table
import pandas as pd


def parse(url, id, search='time-table/student?id='):

    table_list=pd.read_html(url+search+id, attrs = {'id': 'timeTable'}, flavor='lxml')

    df = table_list[0].replace(r'&nbsp','Нет пары', regex=True) # replace the value with NoValue, in case needed further
    df_header=['Day','W1','W2','W3','W4','W5']
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
    df_final.insert(0,'week_group',week_days)

    return df_final


def get_weeks_data(url, id):

    df_final = parse(url, id)

    return df_final.loc[:,['Day', 'W1']].to_markdown(),  df_final.loc[:,['Day', 'W2']].to_markdown(),  df_final.loc[:,['Day', 'W3']].to_markdown(),  df_final.loc[:,['Day', 'W4']].to_markdown(),  df_final.loc[:,['Day', 'W5']].to_markdown()


def get_weeks_data_optimized(url, id):

    df_final = parse(url, id)
    
    return [[df_final.loc[:,['Day']].to_markdown(),  df_final.loc[:,['Day']].to_markdown(),  df_final.loc[:,['Day']].to_markdown(),  df_final.loc[:,['Day']].to_markdown(),  df_final.loc[:,['Day']].to_markdown()],
            [df_final.loc[:,['W1']].to_markdown(),  df_final.loc[:,['W2']].to_markdown(),  df_final.loc[:,['W3']].to_markdown(),  df_final.loc[:,['W4']].to_markdown(),  df_final.loc[:,['W5']].to_markdown()]]


def get_week_data(url, id, week='W1'):

    df_final = parse(url, id)
    
    return df_final.loc[:,['Day', week]].to_markdown()


def get_week_data_optimized(url, id, week='W1'):

    df_final = parse(url, id)

    return [df_final.loc[:,['Day']].to_markdown(),df_final.loc[:,[week]].to_markdown()]