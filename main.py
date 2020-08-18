import bs4
import requests
import vk_api
import pymorphy2
from vk_api.longpoll import VkLongPoll, VkEventType
from bot import VkBot

morph = pymorphy2.MorphAnalyzer()



def get_weather(city):
    # if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 14:
    request = requests.get("https://sinoptik.com.ru/погода-" + city.lower())
    b = bs4.BeautifulSoup(request.text, "html.parser")
    result = dict()
    tags = b.select('.table__temp')
    weather = b.select('.weatherIco')
    pressure = b.select('.table__pressure')
    humidity = b.select('.table__humidity')
    up_and_down = b.select('.ss_wrap')[0].getText()
    result['night'] = [int(tags[0].getText()[:-1]), int(tags[1].getText()[:-1])]
    result['morning'] = [int(tags[2].getText()[:-1]), int(tags[3].getText()[:-1])]
    result['afternoon'] = [int(tags[4].getText()[:-1]), int(tags[5].getText()[:-1])]
    result['evening'] = [int(tags[6].getText()[:-1]), int(tags[7].getText()[:-1])]
    result['night'].append(weather[0]['data-title'])
    result['morning'].append(weather[2]['data-title'])
    result['afternoon'].append(weather[4]['data-title'])
    result['evening'].append(weather[6]['data-title'])
    result['night'].append(pressure[0].getText())
    result['morning'].append(pressure[2].getText())
    result['afternoon'].append(pressure[4].getText())
    result['evening'].append(pressure[6].getText())
    result['night'].append(humidity[0].getText())
    result['morning'].append(humidity[2].getText())
    result['afternoon'].append(humidity[4].getText())
    result['evening'].append(humidity[6].getText())
    result['night'].append(up_and_down)
    result['morning'].append(up_and_down)
    result['afternoon'].append(up_and_down)
    result['evening'].append(up_and_down)


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
    data = get_weather(city)
    city = morph.parse(city)[0].inflect({'loct'}).word.capitalize()
    msg = 'Погода в ' + city
    if 6 >= time >= 0:
        msg += ' на ночь &#128337;&#127769;&#127747;\n'
        msg += data['night'][2] + ' ' + get_smile(data['night'][2]) + '\n'
        symbol = '+' if abs(data['night'][0] + data['night'][1]) / 2 == \
                        ((data['night'][0] + data['night'][1]) / 2) else '-'
        msg += 'Средняя температура  ' + symbol + str((data['night'][0] +
                                                       data['night'][1]) // 2) + '&#176;c &#127777;\n'
        msg += f'Мин  {symbol}{min(data["night"][0], data["night"][1])} &#176;c &#127777;\n'
        msg += f'Макс  {symbol}{max(data["night"][0], data["night"][1])} &#176;c &#127777;\n'
        msg += 'Давление  ' + data['night'][3] + ' мм рт ст &#127757;\n'
        msg += 'Влажность  ' + data['night'][4] + '% &#127793;\n'
        up, t1, down, t2 = data['night'][5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 12 >= time > 6:
        msg += ' на утро &#128344;&#127773;&#127749;\n'
        msg += data['morning'][2] + ' ' + get_smile(data['morning'][2]) + '\n'
        symbol = '+' if abs(data['morning'][0] + data['morning'][1]) / 2 == \
                        ((data['morning'][0] + data['morning'][1]) / 2) else '-'
        msg += 'Средняя температура  ' + symbol + str((data['morning'][0] +
                                                       data['morning'][1]) // 2) + '&#176;c &#127777;\n'
        msg += f'Мин  {symbol}{min(data["morning"][0], data["morning"][1])} &#176;c &#127777;\n'
        msg += f'Макс  {symbol}{max(data["morning"][0], data["morning"][1])} &#176;c &#127777;\n'
        msg += 'Давление  ' + data['morning'][3] + ' мм рт ст &#127758;\n'
        msg += 'Влажность  ' + data['morning'][4] + '% &#127807;\n'
        up, t1, down, t2 = data['morning'][5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 18 >= time > 12:
        msg += ' на день &#128337;&#127774;&#127749;\n'
        msg += data['afternoon'][2] + ' ' + get_smile(data['afternoon'][2]) + '\n'
        symbol = '+' if abs(data['afternoon'][0] + data['afternoon'][1]) / 2 == \
                        ((data['afternoon'][0] + data['afternoon'][1]) / 2) else '-'
        msg += 'Средняя температура  ' + symbol + str((data['afternoon'][0] +
                                                       data['afternoon'][1]) // 2) + '&#176;c &#127777;\n'
        msg += f'Мин  {symbol}{min(data["afternoon"][0], data["afternoon"][1])} &#176;c &#127777;\n'
        msg += f'Макс  {symbol}{max(data["afternoon"][0], data["afternoon"][1])} &#176;c &#127777;\n'
        msg += 'Давление  ' + data['afternoon'][3] + ' мм рт ст &#127759;\n'
        msg += 'Влажность  ' + data['afternoon'][4] + '% &#127795;\n'
        up, t1, down, t2 = data['afternoon'][5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    elif 23 >= time > 18:
        msg += ' на вечер &#128344;&#127772;&#127748;\n'
        msg += data['evening'][2] + ' ' + get_smile(data['evening'][2]) + '\n'
        symbol = '+' if abs(data['evening'][0] + data['evening'][1]) / 2 == \
                        ((data['evening'][0] + data['evening'][1]) / 2) else '-'
        msg += 'Средняя температура  ' + symbol + str((data['evening'][0] +
                                                       data['evening'][1]) // 2) + '&#176;c &#127777;\n'
        msg += f'Мин  {symbol}{min(data["evening"][0], data["evening"][1])} &#176;c &#127777;\n'
        msg += f'Макс  {symbol}{max(data["evening"][0], data["evening"][1])} &#176;c &#127777;\n'
        msg += 'Давление  ' + data['evening'][3] + ' мм рт ст &#127757;\n'
        msg += 'Влажность  ' + data['evening'][4] + '% &#127795;\n'
        up, t1, down, t2 = data['evening'][5].split()
        msg += f'{up}:  {t1} &#127749;\n{down}:  {t2} &#127748;'
        return msg
    return ''

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message, 'random_id': vk_api.utils.get_random_id()})

# API-ключ созданный ранее
'''token = "ba6713c40627ba9281241f8b6471c205ef2947306d20d44fe234454b5352d4aecdac76d24ef7a11bbf3c9"

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