import bs4 as bs4
import requests
import datetime


class VkBot:

    def __init__(self, user_id):
        print("\nСоздан объект бота!")

        self._USER_ID = user_id
        self._USERNAME = self._get_user_name_from_vk_id(user_id)

        self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"]

    def _get_user_name_from_vk_id(self, user_id):
        request = requests.get("https://vk.com/id"+str(user_id))
        bs = bs4.BeautifulSoup(request.text, "html.parser")

        user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])

        return user_name.split()[0]

    def new_message(self, message):

        # Привет
        if message.upper() == self._COMMANDS[0]:
            return f"Привет-привет, {self._USERNAME}!"

        # Погода
        elif message.upper() == self._COMMANDS[1]:
            return self._get_weather()

        # Время
        elif message.upper() == self._COMMANDS[2]:
            return self._get_time()

        # Пока
        elif message.upper() == self._COMMANDS[3]:
            return f"Пока-пока, {self._USERNAME}!"

        else:
            return "Не понимаю о чем вы..."

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        b = bs4.BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    @staticmethod
    def _clean_all_tag_from_str(string_line):

        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """

        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result

    @staticmethod
    def _get_weather(city: str = "санкт-петербург") -> list:
        #if datetime.datetime.now().hour == 17 and datetime.datetime.now().minute == 14:
        request = requests.get("https://sinoptik.com.ru/погода-" + city)
        b = bs4.BeautifulSoup(request.text, "html.parser")
        city += 'е'
        p3 = b.select('.table__temp')
        weather_night = 'от ' + p3[0].getText() + " до " + p3[1].getText()
        weather_morning = 'от ' + p3[2].getText() + " до " + p3[3].getText()
        weather_afternoon = 'от ' + p3[4].getText() + " до " + p3[5].getText()
        weather_evening = 'от ' + p3[6].getText() + " до " + p3[7].getText()
        weather = b.select('.weather__content_tab-icon.d000')
        weather = weather[0]['title']
        result = 'Погода в ' + city + ' на сегодня' + '\n'
        result = result + 'Ночью: ' + weather_night + '\n'
        result = result + 'Утром: ' + weather_morning + '\n'
        result = result + 'Днём: ' + weather_afternoon + '\n'
        result = result + 'Вечером: ' + weather_evening + '\n'
        if weather == 'Ясно':
            weather += ' &#9728;'
        elif weather == 'Небольшая облачность':
            weather += ' &#127780;'
        elif weather == 'Облачно с прояснениями':
            weather += ' &#9925;'
        elif weather == 'Переменная облачность, дождь':
            weather += ' &#127782;'
        elif weather == 'Сплошная облачность':
            weather += ' &#9729;'
        elif weather == 'Гроза':
            weather += ' &#127785;'
        elif 'гроза' in weather.lower() and 'дождь' in weather.lower():
            weather += ' &#9928;'
        elif 'дождь' in weather.lower():
            weather += ' &#127783;'
        elif 'снег' in weather.lower():
            weather += ' &#127784;'
        result += weather
        # temp = b.select('.rSide .description')
        # weather = temp[0].getText()
        # result = result + weather.strip()

        return result
