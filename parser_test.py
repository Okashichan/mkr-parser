from bs4 import BeautifulSoup
import requests
import pandas as pd

week = {'Monday':'Пн',
        'Tuesday':'Вт',
        'Wednesday':'Ср',
        'Thursday':'Чт',
        'Friday':'Пт',
        'Saturday':'Сб',
        'Sunday':'Нд'}

url = 'http://portal.ksada.org:8090/time-table/student?id='


def get_data_two(id, url, search='time-table/student?id='):
    #page = requests.get(url+id)
    
    #soup = BeautifulSoup(page.text, "html.parser")
    #table = soup.find('table')
    #tbody = table.find_all('tr')

    try:
        table_list=pd.read_html(url+search+id)
        tmp = table_list[0].to_string()
    except:
        tmp = 'cringe'
    #print(tmp)
    return tmp

    #days = []

    #for i, t in enumerate(tbody):
    #    if t.find('th', class_='headday'):
    #        days.append(i)

    #print(days)

    #print(table_list[0].iloc[[0]])

    '''page = requests.get(url+id)
    soup = BeautifulSoup(page.text, 'lxml')
    table = soup.select_one('table')
    items = []
    c = 0
    for tr in table.select('tr'):
        th_list = tr.select('th')
        td_list = tr.select('td')

        for th in th_list:
            if th.text != '':
                print(th.text)
            for td in td_list:
                if td.text.strip().replace('&nbsp', '') != '':
                    print(td.text.strip().replace('&nbsp', ''))
    '''



def get_data(url, id):
    page = requests.get(url+id)
    soup = BeautifulSoup(page.text, "html.parser")

    data = []
    days = []
    days_date_info = []
    days_data_info = []
    days_time_info = []
    table = soup.find('table')
    tbody = table.find_all('tr')
    '''
    for t in tbody:
        try:
            tmp1 = t.find('th', class_='headday').getText()
            tmp2 = [tt.getText() for tt in t.find_all('th', class_='headdate')]
            data.append(tmp1, tmp2)
        except:
            #print('No headday or headdate')
            data.append([])

        try:
            tmp1 = t.find('span', class_='lesson').getText()
            tmp2 = t.find('span', class_='start').getText()
            tmp3 = t.find('span', class_='end').getText()
            data.append(tmp1, tmp2, tmp3)
        except:
           #print('No lesson, start, or end')
           data.append([])

        try:
            tmp = [tt.getText().split() for tt in t.find_all('div', class_='lesson-2')]
            data.append(tmp)
        except:
            #print('No lesson-2')
            data.append([])
        else:
            tmp = [tt.getText().split() for tt in t.find_all('div', class_='lesson-1')]
            data.append(tmp)
        finally:
            #print('No lesson-1')
            data.append([])
    '''

    #print(data[0])

    #for d in data:
    #    if not bool(d):
    #        data.remove(d)

    #print(data[0])
    
    for i, t in enumerate(tbody):
        if t.find('th', class_='headday'):
            #tmp1 = t.find('th', class_='headday').getText()
            #tmp2 = [t.getText() for t in t.find_all('th', class_='headdate')]
            #days.append([i, tmp1, tmp2])
            days.append(i)
            #days_date_info.append(tmp1)
            #days_data_info.append(tmp2)

    #days_count.append(0)

    #for i, d in enumerate(days[:-1]):
    #    days_count.append(days[i+1][0]-days[i][0])

    #print(days_count)

    for i, d in enumerate(days[:-1]):
        for t in tbody[days[i]:days[i+1]]:
            '''
            tmp1 = [tt.getText() for tt in t.find_all('th', class_='headday')]
            #print(t)

            try:
                tmp2 = [tt.getText().split() for tt in t.find_all('div', class_='lesson-2')]
                #if not tmp2:
                #    data.append([days_date_info[i], days_data_info[i], days_time_info[i], 'free'])
                #else:
                #    data.append([days_date_info[i], days_data_info[i], days_time_info[i], tmp2])
            except:
                pass
            else:
                tmp3 = [tt.getText().split() for tt in t.find_all('div', class_='lesson-1')]
                #if not tmp3:
                #    data.append([days_date_info[i], days_data_info[i], days_time_info[i], 'free'])
                #else:
                #    data.append([days_date_info[i], days_data_info[i], days_time_info[i], tmp3])
            finally:
               pass

        print(tmp1)
        
        #if not tmp1 or tmp2 or tmp3:
        #    data.append([tmp1, 'free'])
        #else:
        #    data.append([])
            '''


    #[print(d[2]) for d in data]
    #print(data[11])

    #for d in data:
    #    if d[2] != 'free':
    #        #ddd = datetime(int(d[1][0].split('.')[2]), int(d[1][0].split('.')[1]), int(d[1][0].split('.')[0])).strftime('%A')
    #        #print(week[ddd])
    #        print(d[0])
    #        #print([week[datetime(int(d.split('.')[2]), int(d.split('.')[1]), int(d.split('.')[0])).strftime('%A')] for d in d[1]])
    #        print(d[1])
    #        print(d[2])
    #        print(d[3])
    #        break

    #print(tbody[4].find('th', class_='headday').getText())
    #print([t.getText() for t in tbody[4].find_all('th', class_='headdate')])

    #print(tbody[5].find('span', class_='lesson').getText())
    #print(tbody[5].find('span', class_='start').getText())
    #print(tbody[5].find('span', class_='end').getText())

    #print(tbody[5].find('div', class_='lesson-1').getText())
    #print([t.getText().split() for t in tbody[5].find_all('div', class_='lesson-2')])

    #print(len(tbody))


#if __name__ == '__main__':
#    get_data_two(url, '5598')
