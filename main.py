from bs4 import BeautifulSoup
import requests
from time import sleep
import datetime
from datetime import date
import pandas as pd
import csv


StartString = 'day-'
NumLink = 1
date = date.today()
step = 0

for times_code in range(7):

    if times_code == 0:
        Link = 'today'
    elif times_code == 1:
        Link = 'tomorrow'
    elif 2 <= times_code <= 7:
        StartString = 'day-'
        NumLink += 1
        Link = StartString + str(NumLink)

    url = f'https://yandex.ru/pogoda/ru-RU/details/{Link}?lat=56.87801&lon=35.89595&lang=ru&via=dnav'
    response = requests.get(url, headers = {"User-Agent":"Mozilla/5.0"}).text
    sleep(3)
    soup = BeautifulSoup(response, 'html.parser')

    temperatures = soup.find_all('div', class_='sc-72d65afc-5 eGLuAs')
    spans = soup.find_all('span', class_='sc-a9fb3bce-5 jEpyhm')
    blows = soup.find_all('div', class_='sc-72c83b8c-1 jndbzj')
    blow_directions = soup.find_all('span', 'sc-72c83b8c-3 bOxJmJ')
    pressures = soup.find_all('div', class_='sc-784b657f-0 fGIfqX')

    temperature = []
    temperature_feeling = []
    gusts = []
    humidity = []
    blow = []
    blow_direction = []
    pressure = []
    speed = 'м/с'
    time = ['Утром', 'Днём', 'Вечером', 'Ночью']
    words = 'утроденьвечерночьМиллимгслба,: '
    words2 = '()'','

    for item_id, spans in enumerate(spans):
        if item_id <= 3:
            temperature_feeling.append(spans.text)
        elif 3 < item_id <= 7:
            gustsItem = spans.text, speed
            gusts.append(gustsItem)
        elif 7 < item_id <= 11:
            humidity.append(spans.text)
        item_id += 1

    for temperatureItem in temperatures:
        temperature.append(temperatureItem.text)

    for blowsItem in blows:
        blowsItem = blowsItem.text, speed
        blow.append(blowsItem)

    for blow_directionItem in blow_directions:
        blow_direction.append(blow_directionItem.text)

    for weather in pressures:
        newWords = ''.join(char for char in weather.text if char not in words)
        pressureItem = newWords, 'мм рт. ст.'
        pressure.append(pressureItem)

    '''  print('Прогноз погоды на', date)
    i = 0
    current_time = 0
    for n in range(4):
        print(time[current_time])
        print('Температура', temperature[i])
        print('Ощущается как', temperature_feeling[i])
        print('Скорость ветра', *blow[i])
        print('Направление ветра', blow_direction[i])
        print('Порывы ветра', *gusts[i])
        print('Влажность', humidity[i])
        print('Давление', *pressure[i], '\n')

        current_time += 1
        i += 1
'''
    i = 0
    current_time = 0
    map = {}
    id = 0

    for n in range(4):
        map[id] = {}
        map[id]['time'] = time[i]
        map[id]['temperature'] = temperature[i]
        map[id]['temperature_feeling'] = temperature_feeling[i]
        map[id]['gusts'] = gusts[i]
        map[id]['humidity'] = humidity[i]
        map[id]['pressure'] = pressure[i]
        id += 1
        i += 1

    df = pd.DataFrame(map)
    fileName = 'ff.csv'
    df.to_csv(fileName)
    '''if id == 0:
        fileName = 'ff.csv'
        df.to_csv(fileName)
    else:
        df.to_csv('ff.csv', mode='a', index=False)
'''
    date = date + datetime.timedelta(days=1)
    times_code += 1
    step += 1