import bs4
import requests
import vk_api
import pymorphy2
from vk_api.longpoll import VkLongPoll, VkEventType

morph = pymorphy2.MorphAnalyzer()


def get_weather(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    tags = b.select('.weather__content_tab-icon')
    mi, ma = b.select('.min')[0].getText().split(), b.select('.max')[0].getText().split()
    result.append(tags[0]['title'])
    result.append(int(mi[1][:-1]))
    result.append(int(ma[1][:-1]))
    up_and_down = b.select('.ss_wrap')[0].getText()
    result.append(up_and_down)
    return result


def get_weather_night(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    tags = b.select('.table__temp')
    weather = b.select('.weatherIco')
    pressure = b.select('.table__pressure')
    humidity = b.select('.table__humidity')
    up_and_down = b.select('.ss_wrap')[0].getText()
    result.append(int(tags[0].getText()[:-1]))
    result.append(int(tags[1].getText()[:-1]))
    result.append(weather[0]['data-title'])
    result.append(pressure[0].getText())
    result.append(humidity[0].getText())
    result.append(up_and_down)
    return result


def get_weather_morning(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    tags = b.select('.table__temp')
    weather = b.select('.weatherIco')
    pressure = b.select('.table__pressure')
    humidity = b.select('.table__humidity')
    up_and_down = b.select('.ss_wrap')[0].getText()
    result.append(int(tags[2].getText()[:-1]))
    result.append(int(tags[3].getText()[:-1]))
    result.append(weather[2]['data-title'])
    result.append(pressure[2].getText())
    result.append(humidity[2].getText())
    result.append(up_and_down)
    return result


def get_weather_afternoon(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    tags = b.select('.table__temp')
    weather = b.select('.weatherIco')
    pressure = b.select('.table__pressure')
    humidity = b.select('.table__humidity')
    up_and_down = b.select('.ss_wrap')[0].getText()
    result.append(int(tags[4].getText()[:-1]))
    result.append(int(tags[5].getText()[:-1]))
    result.append(weather[4]['data-title'])
    result.append(pressure[4].getText())
    result.append(humidity[4].getText())
    result.append(up_and_down)
    return result


def get_weather_evening(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    tags = b.select('.table__temp')
    weather = b.select('.weatherIco')
    pressure = b.select('.table__pressure')
    humidity = b.select('.table__humidity')
    up_and_down = b.select('.ss_wrap')[0].getText()
    result.append(int(tags[6].getText()[:-1]))
    result.append(int(tags[7].getText()[:-1]))
    result.append(weather[6]['data-title'])
    result.append(pressure[6].getText())
    result.append(humidity[6].getText())
    result.append(up_and_down)
    return result


def get_weather_now(city):
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = []
    img = b.select('.weather__article_main_image')[0].find_all('img')[0]['alt']
    t = int(b.select('.weather__article_main_temp')[0].getText()[2:-3])
    result.append(img)
    result.append(t)
    return result


def get_smile(weather):
    if weather == 'Ясно':
        return ' &#9728;'
    elif weather == 'Небольшая облачность':
        return ' &#127780;'
    elif weather == 'Облачно с прояснениями':
        return ' &#9925;'
    elif weather == 'Переменная облачность, дождь':
        return ' &#127782;'
    elif weather == 'Сплошная облачность':
        return ' &#9729;'
    elif weather == 'Гроза':
        return ' &#127785;'
    elif 'гроза' in weather.lower() and 'дождь' in weather.lower():
        return ' &#9928;'
    elif 'дождь' in weather.lower():
        return ' &#127783;'
    elif 'снег' in weather.lower():
        return ' &#127784;'
    return '&#9729;'


def get_message(city, time=3):
    c = city
    city = morph.parse(city)[0].inflect({'loct'})
    city = city.word.capitalize()
    msg = 'Погода в ' + city
    if 6 >= time >= 0:
        data = get_weather_night(c)
        msg += ' на ночь &#128337;&#127769;&#127747;\n'
        msg += f'{data[2]} {get_smile(data[2])}\n'
        symbol = '+' if abs(data[0] + data[1]) / 2 == \
                        ((data[0] + data[1]) / 2) else '-'
        msg += f'Средняя температура  {symbol}{(data[0] + data[1]) // 2}&#176;c &#127777;\n'
        t1, t2 = min(data[0], data[1]), max(data[0], data[1])
        symbol = '+' if abs(t1) == t1 else '-'
        msg += f'Мин  {symbol}{t1}&#176;c &#127777;\n'
        symbol = '+' if abs(t2) == t2 else '-'
        msg += f'Макс  {symbol}{t2}&#176;c &#127777;\n'
        msg += f'Давление  {data[3]} мм рт ст &#127757;\n'
        msg += f'Влажность  {data[4]}% &#127793;\n'
        up, t1, down, t2 = data[5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 12 >= time > 6:
        data = get_weather_morning(c)
        msg += ' на утро &#128344;&#127773;&#127749;\n'
        msg += f'{data[2]} {get_smile(data[2])}\n'
        symbol = '+' if abs(data[0] + data[1]) / 2 == \
                        ((data[0] + data[1]) / 2) else '-'
        msg += f'Средняя температура  {symbol}{(data[0] + data[1]) // 2}&#176;c &#127777;\n'
        t1, t2 = min(data[0], data[1]), max(data[0], data[1])
        symbol = '+' if abs(t1) == t1 else '-'
        msg += f'Мин  {symbol}{t1}&#176;c &#127777;\n'
        symbol = '+' if abs(t2) == t2 else '-'
        msg += f'Макс  {symbol}{t2}&#176;c &#127777;\n'
        msg += f'Давление  {data[3]} мм рт ст &#127758;\n'
        msg += f'Влажность  {data[4]}% &#127807;\n'
        up, t1, down, t2 = data[5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 18 >= time > 12:
        data = get_weather_afternoon(c)
        msg += ' на день &#128337;&#127774;&#127749;\n'
        msg += f'{data[2]} {get_smile(data[2])}\n'
        symbol = '+' if abs(data[0] + data[1]) / 2 == \
                        ((data[0] + data[1]) / 2) else '-'
        msg += f'Средняя температура  {symbol}{(data[0] + data[1]) // 2}&#176;c &#127777;\n'
        t1, t2 = min(data[0], data[1]), max(data[0], data[1])
        symbol = '+' if abs(t1) == t1 else '-'
        msg += f'Мин  {symbol}{t1}&#176;c &#127777;\n'
        symbol = '+' if abs(t2) == t2 else '-'
        msg += f'Макс  {symbol}{t2}&#176;c &#127777;\n'
        msg += f'Давление  {data[3]} мм рт ст &#127759;\n'
        msg += f'Влажность  {data[4]}% &#127795;\n'
        up, t1, down, t2 = data[5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 23 >= time > 18:
        data = get_weather_evening(c)
        msg += ' на вечер &#128344;&#127772;&#127748;\n'
        msg += f'{data[2]} {get_smile(data[2])}\n'
        symbol = '+' if abs(data[0] + data[1]) / 2 == \
                        ((data[0] + data[1]) / 2) else '-'
        msg += f'Средняя температура  {symbol}{(data[0] + data[1]) // 2}&#176;c &#127777;\n'
        t1, t2 = min(data[0], data[1]), max(data[0], data[1])
        symbol = '+' if abs(t1) == t1 else '-'
        msg += f'Мин  {symbol}{t1}&#176;c &#127777;\n'
        symbol = '+' if abs(t2) == t2 else '-'
        msg += f'Макс  {symbol}{t2}&#176;c &#127777;\n'
        msg += f'Давление  {data[3]} мм рт ст &#127757;\n'
        msg += f'Влажность  {data[4]}% &#127795;\n'
        up, t1, down, t2 = data[5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif time == 25:
        data = get_weather(c)
        msg += ' на сегодня &#127774;&#127749;'
        msg += f'\n{data[0]} {get_smile(data[0])}\n'
        symbol = '+' if abs(data[1] + data[2]) / 2 == \
                        ((data[1] + data[2]) / 2) else '-'
        msg += f'Средняя температура  {symbol}{(data[1] + data[2]) // 2}&#176;c &#127777;\n'
        t1, t2 = data[1], data[2]
        symbol = '+' if abs(t1) == t1 else '-'
        msg += f'Мин  {symbol}{t1}&#176;c &#127777;\n'
        symbol = '+' if abs(t2) == t2 else '-'
        msg += f'Макс  {symbol}{t2}&#176;c &#127777;\n'
        up, t1, down, t2 = data[3].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif time == 26:
        data = get_weather_now(c)
        msg += f' сейчас &#127749;\n'
        msg += f'{data[0]} {get_smile(data[0])}\n'
        symbol = '+'if abs(data[1]) == data[1] else '-'
        msg += f'Температура  {symbol}{data[1]}&#176;c &#127777;'
        return msg
    return ''

'''def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': vk_api.utils.get_random_id()})

# API-ключ созданный ранее
token = "ba6713c40627ba9281241f8b6471c205ef2947306d20d44fe234454b5352d4aecdac76d24ef7a11bbf3c9"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

print("Server started")
while True:
    dgs = vk.method('messages.getConversations')
    people = [item['conversation']['peer']['id'] for item in dgs['items']]
    for i in range(0, len(people)):
        city = vk.method('users.get', {'user_id': people[i], 'fields': ['city']})[0]['city']['title']
        write_msg(people[i], get_message(city))
    break

auto()'''