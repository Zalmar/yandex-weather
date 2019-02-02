from time import sleep

import requests

from bs4 import BeautifulSoup


def get_weather(city):
    weather = {}
    headers = {'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

    url = f'https://yandex.ru/pogoda/{city}'
    while True:
        session = requests.Session()
        r = session.get(url, headers=headers)
        # print(r.text)
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'lxml')
            try:
                divs = soup.find_all('dd', attrs={'class': 'term__value'})
                weather['city'] = city
                weather['temp'] = soup.find('span', attrs={'class': 'temp__value'}).text
                weather['time'] = soup.find('time', attrs={'class': 'time fact__time'}).text
                weather['condition'] = soup.find('div', attrs={'class': 'link__condition day-anchor i-bem'}).text
                weather['real_temp'] = soup.find('dl', attrs={'class': 'term term_orient_h fact__feels-like'}).text
                weather['yesterday_temp'] = soup.find('dl', attrs={
                    'term term_orient_h term_size_wide fact__yesterday'}).text
                weather['wind_speed'] = divs[2].text
                weather['wind_direction'] = soup.find('abbr').text
                weather['humidity'] = divs[3].text
                weather['pressure'] = divs[4].text
                break
            except AttributeError:
                sleep(1)
                continue
        else:
            print('Error')
            break

    weather['city'] = weather['city'].capitalize()
    weather['time'] = weather['time'][-5:]
    weather['real_temp'] = int(string_to_integer(weather['real_temp'][13:-1]))
    weather['temp'] = int(string_to_integer(weather['temp']))
    weather['yesterday_temp'] = int(string_to_integer(weather['yesterday_temp'][17:-1]))
    weather['wind_speed'] = float(string_to_integer(weather['wind_speed'][:(weather['wind_speed'].find('м/с')-1)])
                                  .replace(',', '.'))
    weather['humidity'] = int(weather['humidity'][:-1])
    weather['pressure'] = int(string_to_integer(weather['pressure'][:(weather['pressure'].find('м')-1)]))
    if weather['wind_direction'] == 'В':
        weather['wind_direction'] = 'Восточный'
    elif weather['wind_direction'] == 'С':
        weather['wind_direction'] = 'Северный'
    elif weather['wind_direction'] == 'Ю':
        weather['wind_direction'] = 'Южный'
    elif weather['wind_direction'] == 'З':
        weather['wind_direction'] = 'Западный'
    elif weather['wind_direction'] == 'ЮВ':
        weather['wind_direction'] = 'Юго-восточный'
    elif weather['wind_direction'] == 'ЮЗ':
        weather['wind_direction'] = 'Юго-западный'
    elif weather['wind_direction'] == 'СЗ':
        weather['wind_direction'] = 'Северо-западный'
    elif weather['wind_direction'] == 'СВ':
        weather['wind_direction'] = 'Северо-восточный'
    return weather


def string_to_integer(value):
    if value[0] == '−':
        return -int(value[1:])
    elif value[0] == '+':
        return int(value[1:])
    return value


def string_weather(weather):
    time = weather['time']
    city = weather['city']
    condition = weather['condition']
    temp = weather['temp']
    real_temp = weather['real_temp']
    yesterday_temp = weather['yesterday_temp']
    wind_speed = weather['wind_speed']
    wind_direction = weather['wind_direction']
    humidity = weather['humidity']
    pressure = weather['pressure']

    data = f"""Время: {time}
Город: {city}
        {condition}
Температура: {temp}°C
Ощущается как: {real_temp}°C
Вчера в это время: {yesterday_temp}°C
Ветер: {wind_speed} м/с, {wind_direction}
Влажность: {humidity}%
Давление: {pressure} мм рт. ст.
"""
    return data


if __name__ == '__main__':
    print(string_weather(get_weather('samara')))
