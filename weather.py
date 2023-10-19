import tkinter

import requests
from tkinter import *
from tkinter import font
from PIL import Image, ImageTk, ImageSequence, ImageDraw, ImageFont
from PIL.GifImagePlugin import getheader, getdata

# Создание окна приложения
window = Tk()
window.title('Прогноз погоды')
window.geometry('800x600')
window.iconbitmap('E:\\программирование\\weather\\weathers_gif\\icon.ico')
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
        'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
        'humidity': now_info['main']['humidity'],
        'cloud': now_info['clouds']['all'],
        'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
        'temp_min': round((int(now_info['main']['temp_min']) - 273.15), 2),
        'temp_max': round((int(now_info['main']['temp_max']) - 273.15), 2)
    }


# Настройка приложения
def display_weather():
    global lbl_start, city
    bg_image = Image.open('E:\\программирование\\weather\\weathers_gif\\background.gif')
    bg_start_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(bg_image)]

    def update_gif(k):
        frame = bg_start_image[k]
        k = (k + 1) % len(bg_start_image)
        label_back_start.configure(image=frame)
        window.after(80, update_gif, k)

    label_back_start = Label(window)
    label_back_start.place(relwidth=1, relheight=1)
    update_gif(0)
    lbl_start = Label(window, text='Введите название города:', font=('Arial', 20, 'bold', 'italic'),
                      bg='#99FFFF', fg='#000080')
    lbl_start.place(relx=0.5, rely=0.23, anchor='center')
    lbl_my = Label(window, text='Made by yurokbrat', font=('Arial', 10, 'bold', 'italic'),
                   bg='#99FFFF', fg='#000080')
    lbl_my.place(relx=1, rely=1, anchor='se')
    txt = Entry(window, width=20, font=('Arial', 15, 'bold', 'italic'), bg='white', justify='center')
    txt.place(relx=0.5, rely=0.4, anchor='center')
    global city

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
                              f'Максимальная температура --- {info_weather["temp_max"]}°C.', font=('Arial', 5))

    btn_enter_city = Button(window, text='Ввести', command=clicked, font=('Arial', 12), width=10, height=2,
                            bg='#99FFFF', fg='#003366', bd=2, relief='groove')
    btn_enter_city.place(relx=0.5, rely=0.55, anchor='center')


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
