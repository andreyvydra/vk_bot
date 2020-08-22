import vk_api
import json
from weather import *
from longpool import TOKEN


def get_keyboard(inline=False):
    keyboard = {
        "one_time": False,
        "buttons": [
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"10\"}",
                    "label": "Погода на весь день"
                },
                "color": "positive"
            }],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"10\"}",
                    "label": "День"
                },
                "color": "primary"
            },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"10\"}",
                        "label": "Утро"
                    },
                    "color": "primary"
                }],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"10\"}",
                    "label": "Вечер"
                },
                "color": "primary"
            },
                {
                    "action": {
                        "type": "text",
                        "payload": "{\"button\": \"10\"}",
                        "label": "Ночь"
                    },
                    "color": "primary"
                }],
            [{
                "action": {
                    "type": "text",
                    "payload": "{\"button\": \"10\"}",
                    "label": "Выбрать город"
                },
                "color": "negative"
            }]
        ],
        "inline": inline
    }
    keyboard = json.dumps(keyboard, ensure_ascii=False).encode('utf-8')
    keyboard = str(keyboard.decode('utf-8'))
    return keyboard

def write_msg(user_id, city, time=3):
    vk.method('messages.send',
              {'user_id': user_id, 'message': get_message(city, time), 'random_id': vk_api.utils.get_random_id()})


def write_weather_buttons(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Выберите время или город &#128336;&#127751;',
                                'keyboard': get_keyboard(True),
                                'random_id': vk_api.utils.get_random_id()})


def write_incorrect_msg(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Несуществующая команда команда &#10060;'
                                                               ' Пожалуйста, повторите попытку или введите инфо,'
                                                               ' чтобы получить список команд &#9940;&#9888;',
                                'random_id': vk_api.utils.get_random_id()})
    print('Error: Incorrect input')


def write_incorrect_city(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Некорректное название &#10060; Повторите попытку'
                                                               ' введя команду "Выбрать город" или нажмите'
                                                               ' на аналогичную кнопку &#9940;&#9888;',
                                'random_id': vk_api.utils.get_random_id()})


def write_correct_city(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Город успешно изменён &#9989;&#127961;',
                                'random_id': vk_api.utils.get_random_id()})


def write_city_choice(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Введите город или населённый пункт &#127747;',
                                'random_id': vk_api.utils.get_random_id()})


def write_info(user_id):
    vk.method('messages.send', {'user_id': user_id, 'message': 'Я бот погоды &#129302; \nПо умолчанию погода будет'
                                                               ' подбираться под '
                                                               'город, который указан у тебя в профиле &#127747; \nН'
                                                               'о его всегда можно изменить &#9989;&#9989;&#9989; \nНиже представлен'
                                                               ' список команд,'
                                                               ' которые ты можешь выполнить &#128172;\n'
                                                               '&#11015;&#11015;&#11015;&#11015;&#11015;&#11015;&#11015'
                                                               ';&#11015;&#11015;',
                                'random_id': vk_api.utils.get_random_id()})


vk = vk_api.VkApi(token=TOKEN)


def output_code(code):
    print('Code: ' + code)