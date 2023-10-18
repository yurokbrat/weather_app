import requests
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk

# Создание окна приложения
window = Tk()
window.title = 'Прогноз погоды by yurok'
window.geometry('800x600')
info_weather = {}
city = 'Воронеж'


# Получение информации о погоде
def get_weather(city):
    base = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=a0e0c0ffae85a246ab2fefe8634c1aff'
    result = requests.get(base)
    data = result.json()
    now_info = data['list'][0]
    global info_weather
    info_weather = {
        'now_info': now_info,
        'time_update': now_info['dt_txt'],
        'temp': round((int(now_info['main']['temp']) - 273.15), 2),
        'condition': now_info['weather'][0]['main'],
        'wind': now_info['wind']['speed'],
        'precip': now_info['rain'] if ['rain'] in [now_info] else 0,
        'humidity': now_info['main']['humidity'],
        'cloud': now_info['clouds']['all'],
        'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
        'temp_min': round((int(now_info['main']['temp_min']) - 273.15), 2),
        'temp_max': round((int(now_info['main']['temp_max']) - 273.15), 2)
    }


# Настройка приложения
def display_weather():
    global lbl_start, city
    lbl_start = Label(window, text=f'Введите название города: ', font=('Arial', 15))
    lbl_start.grid(column=0, row=0)
    global city
    txt = Entry(window, width=10)
    txt.grid(column=1, row=0)

    def clicked():
        global city
        city = txt.get()
        get_weather(city)
        lbl_start.config(text=f'{info_weather["time_update"]} в городе {city}: \n'
                              f'Температура --- {info_weather["temp"]}°C,\nСтатус неба --- {info_weather["condition"]},\n'
                              f'Скорость ветра --- {info_weather["wind"]} км/ч,\n'
                              f'Количество осадков за последние 3 часа --- {info_weather["precip"]} мм,\n'
                              f'Влажность --- {info_weather["humidity"]} %,\nОблачность --- {info_weather["cloud"]} %,\n'
                              f'Ощущается как --- {info_weather["feelslike"]}°C,\n'
                              f'Минимальная температура --- {info_weather["temp_min"]}°C,\n'
                              f'Максимальная температура --- {info_weather["temp_max"]}°C.', font=('Arial', 15))

    btn_enter_city = Button(window, text='Ввести', command=clicked)
    btn_enter_city.grid(column=2, row=0)


display_weather()
window.mainloop()

# памятка для себя
"""
1)добавить потом внизу страницы icon by https://icons8.com
2) различные состояния погоды:
API OpenWeather предоставляет разнообразные состояния погоды в поле 'main' внутри массива 'weather'. 
Ниже приведен список основных состояний погоды, которые могут встречаться в этом поле:
Clear (ясно), Clouds (облачно), Drizzle (морось), Rain (дождь), Thunderstorm (гроза), Snow (снег), Mist (туман), 
Fog (густой туман), Smoke (дым), Haze (мгла),Dust (пыль), Sand (песок), Ash (вулканический пепел),Squall (шквал), 
Tornado (торнадо)
Это наиболее общие состояния погоды, но OpenWeather также может предоставлять более детальные описания погодных 
условий в поле 'description', такие как "light rain" (легкий дождь) или "heavy snow" (сильный снег).
"""
