# -*- coding: utf-8 -*-
import tkinter
import requests
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, Text, END, messagebox
from ttkthemes import ThemedTk
from time import strftime
from datetime import datetime
import locale
import os
import sys

base_path = getattr(sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))

# Создание приложения
window = ThemedTk(theme='claim')
window.title('Прогноз погоды')
window.geometry('700x500')
window.wm_resizable(0, 0)
icon_path = os.path.join(base_path, 'weathers_gif', 'icon.ico')
window.iconbitmap(icon_path)
info_weather = {}
city = None
lbl_morning_2 = None
lbl_day_2 = None
lbl_evening_2 = None
lbl_night_2 = None
labels = []
labels_2 = []
labels_3 = []
stop_bg = False


# Получение информации о текущем времени
def get_time():
    current_time = datetime.now().time()
    if current_time < datetime.strptime('06:00:00', '%H:%M:%S').time():
        return "night"
    elif current_time < datetime.strptime('12:00:00', '%H:%M:%S').time():
        return "morning"
    elif current_time < datetime.strptime('18:00:00', '%H:%M:%S').time():
        return "day"
    else:
        return "evening"


time_of_day = get_time()


# Получение информации о погоде в указанном городе
def get_weather_all(city):
    global data
    base = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=a0e0c0ffae85a246ab2fefe8634c1aff'
    result = requests.get(base)
    data = result.json()


# Настройка приложения
def display_weather():
    global lbl_start, btn_enter_city, city, txt_city, lbl_morning, lbl_day, lbl_evening, \
        lbl_night
    locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
    bg_image_path = os.path.join(base_path, 'weathers_gif', 'background.gif')
    bg_image = Image.open(bg_image_path)
    bg_start_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(bg_image)]
    bg_image_change_path = os.path.join(base_path, 'weathers_gif', 'background_2.png')
    bg_image_change = Image.open(bg_image_change_path)
    bg_start_change = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(bg_image_change)]
    anime_image_path = os.path.join(base_path, 'weathers_gif', 'girl.gif')
    anime_image = Image.open(anime_image_path)
    anime_girl_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(anime_image)]
    icon_morning_path = os.path.join(base_path, 'weathers_gif', 'icon_morning.png')
    icon_morning = Image.open(icon_morning_path)
    morning_icon = ImageTk.PhotoImage(icon_morning)
    icon_day_path = os.path.join(base_path, 'weathers_gif', 'icon_day.png')
    icon_day = Image.open(icon_day_path)
    day_icon = ImageTk.PhotoImage(icon_day)
    icon_evening_path = os.path.join(base_path, 'weathers_gif', 'icon_evening.png')
    icon_evening = Image.open(icon_evening_path)
    evening_icon = ImageTk.PhotoImage(icon_evening)
    icon_night_path = os.path.join(base_path, 'weathers_gif', 'icon_night.png')
    icon_night = Image.open(icon_night_path)
    night_icon = ImageTk.PhotoImage(icon_night)

    # Обновление гифки с девочкой
    def update_girl_gif(k):
        frame = anime_girl_image[k]
        k = (k + 1) % len(anime_girl_image)
        label_girl_start.configure(image=frame)
        window.after(80, update_girl_gif, k)

    # Обновление гифки с фоном старта
    def update_bg_gif(k):
        global stop_bg
        if stop_bg:
            return
        frame = bg_start_image[k]
        k = (k + 1) % len(bg_start_image)
        label_back_start.configure(image=frame)
        window.after(50, update_bg_gif, k)

    # Обновление гифки с фоном после ввода города
    def update_bg_2_gif(k):
        global stop_bg
        if stop_bg:
            return
        frame = bg_start_change[k]
        k = (k + 1) % len(bg_start_change)
        label_back_start.configure(image=frame)
        window.after(60, update_bg_2_gif, k)

    # Функция для правильного склонения месяца
    def decline_month(month):
        if month == 1:
            return 'января'
        elif month == 2:
            return 'февраля'
        elif month == 3:
            return 'марта'
        elif month == 4:
            return 'апреля'
        elif month == 5:
            return 'мая'
        elif month == 6:
            return 'июня'
        elif month == 7:
            return 'июля'
        elif month == 8:
            return 'августа'
        elif month == 9:
            return 'сентября'
        elif month == 10:
            return 'октября'
        elif month == 11:
            return 'ноября'
        elif month == 12:
            return 'декабря'

    style = ttk.Style()
    style.configure('Tbutton', padding=5, font=('San Francisco', 12), background='#3498db', foreground='white')
    style.configure('Rounded.TEntry', padding=5, font=('San Francisco', 22), relief='flat',
                    borderwidth=55, background='#6ccccc', focuscolor='#003366', fieldbackground='white')
    label_back_start = Label(window)
    label_back_start.place(relwidth=1, relheight=1)
    update_bg_gif(0)
    label_girl_start = Label(window, borderwidth=0)
    label_girl_start.place(relx=-0.045, rely=0.88)
    update_girl_gif(0)
    lbl_start = Label(window, text='Введите название города', font=('San Francisco', 22),
                      bg='#6ccccc', fg='#333333')
    lbl_start.place(relx=0.5, rely=0.195, anchor='center')
    lbl_my = Label(window, text='Made by yurokbrat', font=('Montserrat', 10, 'italic'), bg='#6ccccc', fg='#333333')
    lbl_my.place(relx=1, rely=1.005, anchor='se')
    txt_city = ttk.Entry(window, style='Rounded.TEntry', width=50, justify='center')
    txt_city.place(relx=0.5, rely=0.5, anchor='center')
    txt_city.icursor(len(txt_city.get()) // 2)
    lbl_morning = None
    lbl_day = None
    lbl_evening = None
    lbl_night = None
    labels_icon = []
    labels_weather = []
    # путь к гифкам
    weather_mapping = {
        800: os.path.join(base_path, 'weathers_gif', 'clear_day.gif'),
        801: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        802: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        803: os.path.join(base_path, 'weathers_gif', 'clouds_high.png'),
        804: os.path.join(base_path, 'weathers_gif', 'clouds_high.png'),
        300: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        301: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        302: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        310: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        311: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        312: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        313: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        314: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        321: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        500: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        501: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        502: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        503: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        504: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        511: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        520: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        521: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        522: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        531: os.path.join(base_path, 'weathers_gif', 'rainfail.gif'),
        200: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        201: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        202: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        210: os.path.join(base_path, 'weathers_gif', 'storm.gif'),
        211: os.path.join(base_path, 'weathers_gif', 'thunderstorm.gif'),
        212: os.path.join(base_path, 'weathers_gif', 'thunderstorm.gif'),
        221: os.path.join(base_path, 'weathers_gif', 'storm.gif'),
        230: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        231: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        232: os.path.join(base_path, 'weathers_gif', 'rain.gif'),
        600: os.path.join(base_path, 'weathers_gif', 'light_snow.gif'),
        601: os.path.join(base_path, 'weathers_gif', 'snow.gif'),
        602: os.path.join(base_path, 'weathers_gif', 'snow.gif'),
        611: os.path.join(base_path, 'weathers_gif', 'light_snow.gif'),
        612: os.path.join(base_path, 'weathers_gif', 'light_snow.gif'),
        613: os.path.join(base_path, 'weathers_gif', 'light_snow.gif'),
        615: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        616: os.path.join(base_path, 'weathers_gif', 'light_rain.gif'),
        620: os.path.join(base_path, 'weathers_gif', 'light_snow.gif'),
        621: os.path.join(base_path, 'weathers_gif', 'snow.gif'),
        622: os.path.join(base_path, 'weathers_gif', 'snow.gif'),
        701: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        711: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        721: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        731: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        741: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        751: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        761: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        762: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        771: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
        781: os.path.join(base_path, 'weathers_gif', 'clouds_low.gif'),
    }

    # Функция обновления гифки с погодой
    def create_weather_gif(weather_path, label):
        weather_open = Image.open(weather_path)
        weather_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(weather_open)]

        def update_weather(k):
            frame = weather_image[k]
            k = (k + 1) % len(weather_image)
            label.configure(image=frame)
            window.after(40, update_weather, k)

        update_weather(0)

    # Нажатие на кнопку и переход к отображению погоды
    def clicked():
        global city, labels, lbl_start, txt_city, txt_weather, txt_name_city, \
            lbl_morning, lbl_day, lbl_evening, lbl_night, stop_bg
        city = txt_city.get()
        get_weather_all(city)
        print(data['cod'])
        if data['cod'] == '200':

            update_bg_2_gif(0)
            stop_bg = True

            def show_time():
                string = strftime('%H:%M:%S')
                label_time.config(text=string)
                label_time.after(1000, show_time)

            label_time = tkinter.Label(window, font=('calibri', 15, 'bold'), background='#6ccccc', foreground='#333333')
            label_time.place(relx=0.0035, rely=0.0275, anchor='w')
            lbl_icon = Label(window, text='icon by https://icons8.com', font=('Montserrat', 8, 'italic'), bg='#6ccccc',
                             fg='#333333')
            lbl_icon.place(relx=1, rely=0.03, anchor='se')
            show_time()
            lbl_morning_icon = Label(window, image=morning_icon, borderwidth=0, highlightthickness=0)
            lbl_morning_icon.place(relx=0.095, rely=0.2, anchor='center')
            lbl_day_icon = Label(window, image=day_icon, borderwidth=0, highlightthickness=0)
            lbl_day_icon.place(relx=0.35, rely=0.2, anchor='center')
            lbl_evening_icon = Label(window, image=evening_icon, borderwidth=0, highlightthickness=0)
            lbl_evening_icon.place(relx=0.605, rely=0.2, anchor='center')
            lbl_night_icon = Label(window, image=night_icon, borderwidth=0, highlightthickness=0)
            lbl_night_icon.place(relx=0.855, rely=0.2, anchor='center')
            lbl_morning = Label(window, text='Утро', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
            lbl_morning.place(relx=0.095, rely=0.1275, anchor='center')
            lbl_day = Label(window, text='День', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
            lbl_day.place(relx=0.35, rely=0.1275, anchor='center')
            lbl_evening = Label(window, text='Вечер', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
            lbl_evening.place(relx=0.605, rely=0.1275, anchor='center')
            lbl_night = Label(window, text='Ночь', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
            lbl_night.place(relx=0.855, rely=0.1275, anchor='center')
            lbl_start.place_forget()
            txt_city.place_forget()
            labels.extend([label_time, lbl_icon, lbl_morning_icon, lbl_day_icon, lbl_evening_icon, lbl_night_icon])
            # Прогноз погоды, если сейчас утро
            if time_of_day == 'morning':
                now_info = data['list'][0]
                info_weather_morning = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][2]
                info_weather_day = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][4]
                info_weather_evening = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][6]
                info_weather_night = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                label_weather_morning = Label(window, borderwidth=0)
                if info_weather_morning['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_morning['condition']]
                    create_weather_gif(weather_path, label_weather_morning)
                    label_weather_morning.place(relx=0.0585, rely=0.315)
                    print(info_weather_morning['condition'])
                label_weather_day = Label(window, borderwidth=0)
                if info_weather_day['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_day['condition']]
                    create_weather_gif(weather_path, label_weather_day)
                    label_weather_day.place(relx=0.315, rely=0.315)
                label_weather_evening = Label(window, borderwidth=0)
                if info_weather_evening['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_evening['condition']]
                    create_weather_gif(weather_path, label_weather_evening)
                    label_weather_evening.place(relx=0.565, rely=0.315)
                label_weather_night = Label(window, borderwidth=0)
                if info_weather_night['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_night['condition']]
                    create_weather_gif(weather_path, label_weather_night)
                    label_weather_night.place(relx=0.815, rely=0.315)
                date_object = datetime.strptime(info_weather_morning["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_morning = Text(window, wrap="word", height=8.5, width=33,
                                           bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_morning.place(relx=0.01, rely=0.6175, anchor='w')
                txt_weather_morning.delete(1.0, END)
                txt_weather_morning.insert(END, f'{formatted_date}\n\n'
                                                f'Температура — {info_weather_morning["temp"]}°C\n'
                                                f'Скорость ветра — {info_weather_morning["wind"]} км/ч\n'
                                                f'Вероятность осадков — {info_weather_morning["pop"]} %\n'
                                                f'Осадки за 3 часа — {info_weather_morning["precip"]} мм\n'
                                                f'Влажность — {info_weather_morning["humidity"]} %\n'
                                                f'Облачность — {info_weather_morning["cloud"]} %\n'
                                                f'Ощущается — {info_weather_morning["feelslike"]}°C\n')
                txt_weather_morning.tag_add('bold', '1.0', '1.end')
                txt_weather_morning.tag_add('italic', '2.0', 'end')
                txt_weather_morning.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_morning.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_day["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_day = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                       bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_day.place(relx=0.255, rely=0.6175, anchor='w')
                txt_weather_day.delete(1.0, END)
                txt_weather_day.insert(END, f'{formatted_date}\n\n'
                                            f'Температура — {info_weather_day["temp"]}°C\n'
                                            f'Скорость ветра — {info_weather_day["wind"]} км/ч\n'
                                            f'Вероятность осадков — {info_weather_day["pop"]} %\n'
                                            f'Осадки за 3 часа — {info_weather_day["precip"]} мм\n'
                                            f'Влажность — {info_weather_day["humidity"]} %\n'
                                            f'Облачность — {info_weather_day["cloud"]} %\n'
                                            f'Ощущается — {info_weather_day["feelslike"]}°C\n')
                txt_weather_day.tag_add('bold', '1.0', '1.end')
                txt_weather_day.tag_add('italic', '2.0', 'end')
                txt_weather_day.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_day.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_evening["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_evening = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                           bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_evening.place(relx=0.505, rely=0.6175, anchor='w')
                txt_weather_evening.delete(1.0, END)
                txt_weather_evening.insert(END, f'{formatted_date}\n\n'
                                                f'Температура — {info_weather_evening["temp"]}°C\n'
                                                f'Скорость ветра — {info_weather_evening["wind"]} км/ч\n'
                                                f'Вероятность осадков — {info_weather_evening["pop"]} %\n'
                                                f'Осадки за 3 часа — {info_weather_evening["precip"]} мм\n'
                                                f'Влажность — {info_weather_evening["humidity"]} %\n'
                                                f'Облачность — {info_weather_evening["cloud"]} %\n'
                                                f'Ощущается — {info_weather_evening["feelslike"]}°C\n')
                txt_weather_evening.tag_add('bold', '1.0', '1.end')
                txt_weather_evening.tag_add('italic', '2.0', 'end')
                txt_weather_evening.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_evening.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_night["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_night = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                         bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_night.place(relx=0.755, rely=0.6175, anchor='w')
                txt_weather_night.delete(1.0, END)
                txt_weather_night.insert(END, f'{formatted_date}\n\n'
                                              f'Температура — {info_weather_night["temp"]}°C\n'
                                              f'Скорость ветра — {info_weather_night["wind"]} км/ч\n'
                                              f'Вероятность осадков — {info_weather_night["pop"]} %\n'
                                              f'Осадки за 3 часа — {info_weather_night["precip"]} мм\n'
                                              f'Влажность — {info_weather_night["humidity"]} %\n'
                                              f'Облачность — {info_weather_night["cloud"]} %\n'
                                              f'Ощущается — {info_weather_night["feelslike"]}°C\n')
                txt_weather_night.tag_add('bold', '1.0', '1.end')
                txt_weather_night.tag_add('italic', '2.0', 'end')
                txt_weather_night.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_night.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_morning["time_update"]}',
                                        font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
                lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
                labels.extend([lbl_morning, lbl_day, lbl_evening, lbl_night,
                               txt_weather_morning, txt_weather_day, txt_weather_evening, txt_weather_night,
                               lbl_last_update])
                labels_weather.extend([label_weather_morning, label_weather_day, label_weather_evening,
                                       label_weather_night])
            # Прогноз погоды, если сейчас день
            if time_of_day == 'day':
                lbl_morning_icon.place_forget()
                lbl_day_icon.place(relx=0.115, rely=0.2, anchor='center')
                lbl_evening_icon.place(relx=0.475, rely=0.2, anchor='center')
                lbl_night_icon.place(relx=0.835, rely=0.2, anchor='center')
                lbl_morning.place_forget()
                lbl_day.place(relx=0.115, rely=0.1275, anchor='center')
                lbl_evening.place(relx=0.475, rely=0.1275, anchor='center')
                lbl_night.place(relx=0.835, rely=0.1275, anchor='center')
                now_info = data['list'][0]
                info_weather_day = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][2]
                info_weather_evening = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][4]
                info_weather_night = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                label_weather_day = Label(window, borderwidth=0)
                if info_weather_day['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_day['condition']]
                    create_weather_gif(weather_path, label_weather_day)
                    label_weather_day.place(relx=0.0825, rely=0.315)
                label_weather_evening = Label(window, borderwidth=0)
                if info_weather_evening['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_evening['condition']]
                    create_weather_gif(weather_path, label_weather_evening)
                    label_weather_evening.place(relx=0.44, rely=0.315)
                label_weather_night = Label(window, borderwidth=0)
                if info_weather_night['condition'] in weather_mapping:
                    if info_weather_night['condition'] == 800:
                        weather_path = os.path.join(base_path, 'weathers_gif', 'clear_night.gif')
                    else:
                        weather_path = weather_mapping[info_weather_night['condition']]
                    create_weather_gif(weather_path, label_weather_night)
                    label_weather_night.place(relx=0.8, rely=0.315)
                date_object = datetime.strptime(info_weather_day["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_day = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                       bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_day.place(relx=0.0375, rely=0.6175, anchor='w')
                txt_weather_day.delete(1.0, END)
                txt_weather_day.insert(END, f'{formatted_date}\n\n'
                                            f'Температура — {info_weather_day["temp"]}°C\n'
                                            f'Скорость ветра — {info_weather_day["wind"]} км/ч\n'
                                            f'Вероятность осадков — {info_weather_day["pop"]} %\n'
                                            f'Осадки за 3 часа — {info_weather_day["precip"]} мм\n'
                                            f'Влажность — {info_weather_day["humidity"]} %\n'
                                            f'Облачность — {info_weather_day["cloud"]} %\n'
                                            f'Ощущается — {info_weather_day["feelslike"]}°C\n')
                txt_weather_day.tag_add('bold', '1.0', '1.end')
                txt_weather_day.tag_add('italic', '2.0', 'end')
                txt_weather_day.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_day.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_evening["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_evening = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                           bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_evening.place(relx=0.395, rely=0.6175, anchor='w')
                txt_weather_evening.delete(1.0, END)
                txt_weather_evening.insert(END, f'{formatted_date}\n\n'
                                                f'Температура — {info_weather_evening["temp"]}°C\n'
                                                f'Скорость ветра — {info_weather_evening["wind"]} км/ч\n'
                                                f'Вероятность осадков — {info_weather_evening["pop"]} %\n'
                                                f'Осадки за 3 часа — {info_weather_evening["precip"]} мм\n'
                                                f'Влажность — {info_weather_evening["humidity"]} %\n'
                                                f'Облачность — {info_weather_evening["cloud"]} %\n'
                                                f'Ощущается — {info_weather_evening["feelslike"]}°C\n')
                txt_weather_evening.tag_add('bold', '1.0', '1.end')
                txt_weather_evening.tag_add('italic', '2.0', 'end')
                txt_weather_evening.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_evening.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_night["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_night = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                         bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_night.place(relx=0.7375, rely=0.6175, anchor='w')
                txt_weather_night.delete(1.0, END)
                txt_weather_night.insert(END, f'{formatted_date}\n\n'
                                              f'Температура — {info_weather_night["temp"]}°C\n'
                                              f'Скорость ветра — {info_weather_night["wind"]} км/ч\n'
                                              f'Вероятность осадков — {info_weather_night["pop"]} %\n'
                                              f'Осадки за 3 часа — {info_weather_night["precip"]} мм\n'
                                              f'Влажность — {info_weather_night["humidity"]} %\n'
                                              f'Облачность — {info_weather_night["cloud"]} %\n'
                                              f'Ощущается — {info_weather_night["feelslike"]}°C\n')
                txt_weather_night.tag_add('bold', '1.0', '1.end')
                txt_weather_night.tag_add('italic', '2.0', 'end')
                txt_weather_night.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_night.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_day["time_update"]}',
                                        font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
                lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
                labels.extend([lbl_day, lbl_evening, lbl_night, txt_weather_day, txt_weather_evening, txt_weather_night,
                               lbl_last_update])
                labels_weather.extend([label_weather_day, label_weather_evening, label_weather_night])
            # Прогноз погоды, если сейчас вечер
            if time_of_day == 'evening':
                lbl_morning_icon.place_forget()
                lbl_day_icon.place_forget()
                lbl_evening_icon.place(relx=0.21, rely=0.2, anchor='center')
                lbl_night_icon.place(relx=0.76, rely=0.2, anchor='center')
                lbl_morning.place_forget()
                lbl_day.place_forget()
                lbl_evening.place(relx=0.21, rely=0.1275, anchor='center')
                lbl_night.place(relx=0.76, rely=0.1275, anchor='center')
                now_info = data['list'][0]
                info_weather_evening = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                now_info = data['list'][2]
                info_weather_night = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                label_weather_evening = Label(window, borderwidth=0)
                if info_weather_evening['condition'] in weather_mapping:
                    weather_path = weather_mapping[info_weather_evening['condition']]
                    create_weather_gif(weather_path, label_weather_evening)
                    label_weather_evening.place(relx=0.175, rely=0.315)
                label_weather_night = Label(window, borderwidth=0)
                if info_weather_night['condition'] in weather_mapping:
                    if info_weather_night['condition'] == 800:
                        weather_path = os.path.join(base_path, 'weathers_gif', 'clear_night.gif')
                    else:
                        weather_path = weather_mapping[info_weather_night['condition']]
                    create_weather_gif(weather_path, label_weather_night)
                    label_weather_night.place(relx=0.725, rely=0.315)
                date_object = datetime.strptime(info_weather_evening["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                formatted_date = info_weather_evening["time_update"]
                txt_weather_evening = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                           bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_evening.place(relx=0.125, rely=0.6175, anchor='w')
                txt_weather_evening.delete(1.0, END)
                txt_weather_evening.insert(END, f'{formatted_date}\n\n'
                                                f'Температура — {info_weather_evening["temp"]}°C\n'
                                                f'Скорость ветра — {info_weather_evening["wind"]} км/ч\n'
                                                f'Вероятность осадков — {info_weather_evening["pop"]} %\n'
                                                f'Осадки за 3 часа — {info_weather_evening["precip"]} мм\n'
                                                f'Влажность — {info_weather_evening["humidity"]} %\n'
                                                f'Облачность — {info_weather_evening["cloud"]} %\n'
                                                f'Ощущается — {info_weather_evening["feelslike"]}°C\n')
                txt_weather_evening.tag_add('bold', '1.0', '1.end')
                txt_weather_evening.tag_add('italic', '2.0', 'end')
                txt_weather_evening.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_evening.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                date_object = datetime.strptime(info_weather_night["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_night = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                         bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_night.place(relx=0.665, rely=0.6175, anchor='w')
                txt_weather_night.delete(1.0, END)
                txt_weather_night.insert(END, f'{formatted_date}\n\n'
                                              f'Температура — {info_weather_night["temp"]}°C\n'
                                              f'Скорость ветра — {info_weather_night["wind"]} км/ч\n'
                                              f'Вероятность осадков — {info_weather_night["pop"]} %\n'
                                              f'Осадки за 3 часа — {info_weather_night["precip"]} мм\n'
                                              f'Влажность — {info_weather_night["humidity"]} %\n'
                                              f'Облачность — {info_weather_night["cloud"]} %\n'
                                              f'Ощущается — {info_weather_night["feelslike"]}°C\n')
                txt_weather_night.tag_add('bold', '1.0', '1.end')
                txt_weather_night.tag_add('italic', '2.0', 'end')
                txt_weather_night.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_night.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_evening["time_update"]}',
                                        font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
                lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
                labels.extend([lbl_evening, lbl_night, txt_weather_evening, txt_weather_night,
                               lbl_last_update])
                labels_weather.extend([label_weather_evening, label_weather_night])
            # Прогноз погоды, если сейчас ночь
            if time_of_day == 'night':
                lbl_morning_icon.place_forget()
                lbl_day_icon.place_forget()
                lbl_evening_icon.place_forget()
                lbl_night_icon.place(relx=0.5, rely=0.2, anchor='center')
                lbl_morning.place_forget()
                lbl_day.place_forget()
                lbl_evening.place_forget()
                lbl_night.place(relx=0.5, rely=0.1275, anchor='center')
                now_info = data['list'][0]
                info_weather_night = {
                    'now_info': now_info,
                    'time_update': now_info['dt_txt'],
                    'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                    'condition': now_info['weather'][0]['id'],
                    'wind': now_info['wind']['speed'],
                    'pop': round((now_info['pop'] * 100), 2),
                    'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                    'humidity': now_info['main']['humidity'],
                    'cloud': now_info['clouds']['all'],
                    'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
                }
                label_weather_night = Label(window, borderwidth=0)
                if info_weather_night['condition'] in weather_mapping:
                    if info_weather_night['condition'] == 800:
                        weather_path = os.path.join(base_path, 'weathers_gif', 'clear_night.gif')
                    else:
                        weather_path = weather_mapping[info_weather_night['condition']]
                    create_weather_gif(weather_path, label_weather_night)
                    label_weather_night.place(relx=0.465, rely=0.315)
                date_object = datetime.strptime(info_weather_night["time_update"], '%Y-%m-%d %H:%M:%S')
                month_number = date_object.month
                declined_month = decline_month(month_number)
                formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
                txt_weather_night = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                         bg='#6ccccc', fg='#333333', borderwidth=0)
                txt_weather_night.place(relx=0.4, rely=0.6175, anchor='w')
                txt_weather_night.delete(1.0, END)
                txt_weather_night.insert(END, f'{formatted_date}\n\n'
                                              f'Температура — {info_weather_night["temp"]}°C\n'
                                              f'Скорость ветра — {info_weather_night["wind"]} км/ч\n'
                                              f'Вероятность осадков — {info_weather_night["pop"]} %\n'
                                              f'Осадки за 3 часа — {info_weather_night["precip"]} мм\n'
                                              f'Влажность — {info_weather_night["humidity"]} %\n'
                                              f'Облачность — {info_weather_night["cloud"]} %\n'
                                              f'Ощущается — {info_weather_night["feelslike"]}°C\n')
                txt_weather_night.tag_add('bold', '1.0', '1.end')
                txt_weather_night.tag_add('italic', '2.0', 'end')
                txt_weather_night.tag_configure('bold', font=('San Francisco', 10, 'bold'))
                txt_weather_night.tag_configure('italic', font=('San Francisco', 8, 'italic'))
                lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_night["time_update"]}',
                                        font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
                lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
                labels.extend([lbl_night, txt_weather_night, lbl_last_update])
                labels_weather.append(label_weather_night)
            labels_icon.extend([lbl_morning_icon, lbl_day_icon, lbl_evening_icon, lbl_night_icon])
            txt_name_city = Text(window, font=('San Francisco', 17,), wrap="word", height=1,
                                 width=30, bg='#6ccccc', fg='#333333', borderwidth=0)
            txt_name_city.tag_configure('center', justify='center')
            txt_name_city.tag_add('center', '1.0', 'end')
            txt_name_city.place(relx=0.575, rely=0.05, anchor='center')
            txt_name_city.insert(END, f'Вы выбрали город {city}')
            btn_enter_city.place_forget()
            btn_enter_city_first_day = ttk.Button(window, text='\nВвести новый город\n', command=clicked_back,
                                                  style="TButton", width=23)
            btn_enter_city_first_day.place(relx=0.15, rely=0.825, anchor='center')
            btn_enter_city_second_day = ttk.Button(window, text='\nПрогноз на завтра\n', command=clicked_1_day,
                                                   style="TButton", width=23)
            btn_enter_city_second_day.place(relx=0.5, rely=0.825, anchor='center')
            btn_enter_city_third_day = ttk.Button(window, text='\nПрогноз на послезавтра\n', command=clicked_2_day,
                                                  style="TButton", width=23)
            btn_enter_city_third_day.place(relx=0.85, rely=0.825, anchor='center')
            labels.extend(
                [txt_name_city, btn_enter_city_first_day, btn_enter_city_second_day, btn_enter_city_third_day])
        else:
            messagebox.showerror(title=f'Ошибка при вводе города {city}', message=f'Ошибка «{data["message"]}»')
        city = txt_city.get()
        get_weather_all(city)

    btn_enter_city = ttk.Button(window, text='\nВвести\n', command=clicked, style="TButton", width=15)
    btn_enter_city.place(relx=0.5, rely=0.7, anchor='center')

    # Нажатие на кнопку «Прогноз на завтра»
    def clicked_1_day():
        global city, labels_2, lbl_morning, lbl_day, lbl_evening, lbl_night, lbl_morning_2, lbl_day_2, \
            lbl_evening_2, lbl_night_2

        for label in labels_weather:
            label.destroy()
        for label in labels_icon:
            label.destroy()
        if lbl_morning:
            lbl_morning.destroy()
        if lbl_day:
            lbl_day.destroy()
        if lbl_evening:
            lbl_evening.destroy()
        if lbl_night:
            lbl_night.destroy()
        if time_of_day == 'morning':
            now_info_11_morning = data['list'][7]
            now_info_12_day = data['list'][9]
            now_info_13_evening = data['list'][11]
            now_info_14_night = data['list'][13]
        if time_of_day == 'day':
            now_info_11_morning = data['list'][6]
            now_info_12_day = data['list'][8]
            now_info_13_evening = data['list'][10]
            now_info_14_night = data['list'][12]
        if time_of_day == 'evening':
            now_info_11_morning = data['list'][4]
            now_info_12_day = data['list'][6]
            now_info_13_evening = data['list'][8]
            now_info_14_night = data['list'][10]
        if time_of_day == 'night':
            now_info_11_morning = data['list'][2]
            now_info_12_day = data['list'][4]
            now_info_13_evening = data['list'][6]
            now_info_14_night = data['list'][8]
        now_info_know_time = data['list'][0]
        time_update = now_info_know_time['dt_txt']
        get_weather_all(city)
        txt_name_city.delete(1.0, END)
        txt_name_city.insert(END, f'Вы выбрали город {city}')
        lbl_morning_icon = Label(window, image=morning_icon, borderwidth=0, highlightthickness=0)
        lbl_morning_icon.place(relx=0.095, rely=0.2, anchor='center')
        lbl_day_icon = Label(window, image=day_icon, borderwidth=0, highlightthickness=0)
        lbl_day_icon.place(relx=0.35, rely=0.2, anchor='center')
        lbl_evening_icon = Label(window, image=evening_icon, borderwidth=0, highlightthickness=0)
        lbl_evening_icon.place(relx=0.605, rely=0.2, anchor='center')
        lbl_night_icon = Label(window, image=night_icon, borderwidth=0, highlightthickness=0)
        lbl_night_icon.place(relx=0.855, rely=0.2, anchor='center')
        lbl_morning_2 = Label(window, text='Утро', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_morning_2.place(relx=0.095, rely=0.1275, anchor='center')
        lbl_day_2 = Label(window, text='День', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_day_2.place(relx=0.35, rely=0.1275, anchor='center')
        lbl_evening_2 = Label(window, text='Вечер', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_evening_2.place(relx=0.605, rely=0.1275, anchor='center')
        lbl_night_2 = Label(window, text='Ночь', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_night_2.place(relx=0.855, rely=0.1275, anchor='center')

        info_weather_1_morning = {
            'now_info': now_info_11_morning,
            'time_update': now_info_11_morning['dt_txt'],
            'temp': round((int(now_info_11_morning['main']['temp']) - 273.15), 2),
            'condition': now_info_11_morning['weather'][0]['id'],
            'wind': now_info_11_morning['wind']['speed'],
            'pop': round((now_info_11_morning['pop'] * 100), 2),
            'precip': now_info_11_morning['rain']['3h'] if 'rain' in now_info_11_morning else 0,
            'humidity': now_info_11_morning['main']['humidity'],
            'cloud': now_info_11_morning['clouds']['all'],
            'feelslike': round((int(now_info_11_morning['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_day = {
            'now_info': now_info_12_day,
            'time_update': now_info_12_day['dt_txt'],
            'temp': round((int(now_info_12_day['main']['temp']) - 273.15), 2),
            'condition': now_info_12_day['weather'][0]['id'],
            'wind': now_info_12_day['wind']['speed'],
            'pop': round((now_info_12_day['pop'] * 100), 2),
            'precip': now_info_12_day['rain']['3h'] if 'rain' in now_info_12_day else 0,
            'humidity': now_info_12_day['main']['humidity'],
            'cloud': now_info_12_day['clouds']['all'],
            'feelslike': round((int(now_info_12_day['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_evening = {
            'now_info': now_info_13_evening,
            'time_update': now_info_13_evening['dt_txt'],
            'temp': round((int(now_info_13_evening['main']['temp']) - 273.15), 2),
            'condition': now_info_13_evening['weather'][0]['id'],
            'wind': now_info_13_evening['wind']['speed'],
            'pop': round((now_info_13_evening['pop'] * 100), 2),
            'precip': now_info_13_evening['rain']['3h'] if 'rain' in now_info_13_evening else 0,
            'humidity': now_info_13_evening['main']['humidity'],
            'cloud': now_info_13_evening['clouds']['all'],
            'feelslike': round((int(now_info_13_evening['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_night = {
            'now_info': now_info_14_night,
            'time_update': now_info_14_night['dt_txt'],
            'temp': round((int(now_info_14_night['main']['temp']) - 273.15), 2),
            'condition': now_info_14_night['weather'][0]['id'],
            'wind': now_info_14_night['wind']['speed'],
            'pop': round((now_info_14_night['pop'] * 100), 2),
            'precip': now_info_14_night['rain']['3h'] if 'rain' in now_info_14_night else 0,
            'humidity': now_info_14_night['main']['humidity'],
            'cloud': now_info_14_night['clouds']['all'],
            'feelslike': round((int(now_info_14_night['main']['feels_like']) - 273.15), 2),
        }
        label_weather_morning_1 = Label(window, borderwidth=0)
        if info_weather_1_morning['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_morning['condition']]
            create_weather_gif(weather_path, label_weather_morning_1)
            label_weather_morning_1.place(relx=0.0585, rely=0.315)
        label_weather_day_1 = Label(window, borderwidth=0)
        if info_weather_1_day['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_day['condition']]
            create_weather_gif(weather_path, label_weather_day_1)
            label_weather_day_1.place(relx=0.315, rely=0.315)
        label_weather_evening_1 = Label(window, borderwidth=0)
        if info_weather_1_evening['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_evening['condition']]
            create_weather_gif(weather_path, label_weather_evening_1)
            label_weather_evening_1.place(relx=0.565, rely=0.315)
        label_weather_night_1 = Label(window, borderwidth=0)
        if info_weather_1_night['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_night['condition']]
            create_weather_gif(weather_path, label_weather_night_1)
            label_weather_night_1.place(relx=0.815, rely=0.315)
        date_object = datetime.strptime(info_weather_1_morning["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_morning = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                   bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_morning.place(relx=0.005, rely=0.6175, anchor='w')
        txt_weather_morning.delete(1.0, END)
        txt_weather_morning.insert(END, f'{formatted_date}\n\n'
                                        f'Температура — {info_weather_1_morning["temp"]}°C\n'
                                        f'Скорость ветра — {info_weather_1_morning["wind"]} км/ч\n'
                                        f'Вероятность осадков — {info_weather_1_morning["pop"]} %\n'
                                        f'Осадки за 3 часа — {info_weather_1_morning["precip"]} мм\n'
                                        f'Влажность — {info_weather_1_morning["humidity"]} %\n'
                                        f'Облачность — {info_weather_1_morning["cloud"]} %\n'
                                        f'Ощущается — {info_weather_1_morning["feelslike"]}°C\n')
        txt_weather_morning.tag_add('bold', '1.0', '1.end')
        txt_weather_morning.tag_add('italic', '2.0', 'end')
        txt_weather_morning.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_morning.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_day["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_day_1 = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                 bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_day_1.place(relx=0.255, rely=0.6175, anchor='w')
        txt_weather_day_1.delete(1.0, END)
        txt_weather_day_1.insert(END, f'{formatted_date}\n\n'
                                      f'Температура — {info_weather_1_day["temp"]}°C\n'
                                      f'Скорость ветра — {info_weather_1_day["wind"]} км/ч\n'
                                      f'Вероятность осадков — {info_weather_1_day["pop"]} %\n'
                                      f'Осадки за 3 часа — {info_weather_1_day["precip"]} мм\n'
                                      f'Влажность — {info_weather_1_day["humidity"]} %\n'
                                      f'Облачность — {info_weather_1_day["cloud"]} %\n'
                                      f'Ощущается — {info_weather_1_day["feelslike"]}°C\n')
        txt_weather_day_1.tag_add('bold', '1.0', '1.end')
        txt_weather_day_1.tag_add('italic', '2.0', 'end')
        txt_weather_day_1.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_day_1.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_evening["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_evening_1 = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                     bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_evening_1.place(relx=0.505, rely=0.6175, anchor='w')
        txt_weather_evening_1.delete(1.0, END)
        txt_weather_evening_1.insert(END, f'{formatted_date}\n\n'
                                          f'Температура — {info_weather_1_evening["temp"]}°C\n'
                                          f'Скорость ветра — {info_weather_1_evening["wind"]} км/ч\n'
                                          f'Вероятность осадков — {info_weather_1_evening["pop"]} %\n'
                                          f'Осадки за 3 часа — {info_weather_1_evening["precip"]} мм\n'
                                          f'Влажность — {info_weather_1_evening["humidity"]} %\n'
                                          f'Облачность — {info_weather_1_evening["cloud"]} %\n'
                                          f'Ощущается — {info_weather_1_evening["feelslike"]}°C\n')
        txt_weather_evening_1.tag_add('bold', '1.0', '1.end')
        txt_weather_evening_1.tag_add('italic', '2.0', 'end')
        txt_weather_evening_1.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_evening_1.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_night["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_night_1 = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                   bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_night_1.place(relx=0.755, rely=0.6175, anchor='w')
        txt_weather_night_1.delete(1.0, END)
        txt_weather_night_1.insert(END, f'{formatted_date}\n\n'
                                        f'Температура — {info_weather_1_night["temp"]}°C\n'
                                        f'Скорость ветра — {info_weather_1_night["wind"]} км/ч\n'
                                        f'Вероятность осадков — {info_weather_1_night["pop"]} %\n'
                                        f'Осадки за 3 часа — {info_weather_1_night["precip"]} мм\n'
                                        f'Влажность — {info_weather_1_night["humidity"]} %\n'
                                        f'Облачность — {info_weather_1_night["cloud"]} %\n'
                                        f'Ощущается — {info_weather_1_night["feelslike"]}°C\n')
        txt_weather_night_1.tag_add('bold', '1.0', '1.end')
        txt_weather_night_1.tag_add('italic', '2.0', 'end')
        txt_weather_night_1.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_night_1.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        lbl_last_update = Label(window, text=f'Информация была обновлена {time_update}',
                                font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
        lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
        labels_2.extend([txt_name_city, lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2, txt_weather_morning,
                         txt_weather_day_1, txt_weather_evening_1, txt_weather_night_1, lbl_last_update,
                         lbl_morning_icon, lbl_day_icon, lbl_evening_icon, lbl_night_icon])
        labels_weather.extend([label_weather_morning_1, label_weather_day_1,
                               label_weather_evening_1, label_weather_night_1])

    # Кнопка «Прогноз на послезавтра»
    def clicked_2_day():
        global city, labels_3, lbl_morning, lbl_day, lbl_evening, lbl_night, lbl_morning_2, lbl_day_2, lbl_evening_2, \
            lbl_night_2, txt_weather_morning, lbl_morning_icon, lbl_day_icon, lbl_evening_icon, lbl_night_icon

        for label in labels_weather:
            label.destroy()
        if lbl_morning:
            lbl_morning.destroy()
        if lbl_day:
            lbl_day.destroy()
        if lbl_evening:
            lbl_evening.destroy()
        if lbl_night:
            lbl_night.destroy()
        if time_of_day == 'morning':
            now_info_21_morning = data['list'][15]
            now_info_22_day = data['list'][17]
            now_info_23_evening = data['list'][19]
            now_info_24_night = data['list'][28]
        if time_of_day == 'day':
            now_info_21_morning = data['list'][14]
            now_info_22_day = data['list'][16]
            now_info_23_evening = data['list'][18]
            now_info_24_night = data['list'][20]
        if time_of_day == 'evening':
            now_info_21_morning = data['list'][12]
            now_info_22_day = data['list'][14]
            now_info_23_evening = data['list'][16]
            now_info_24_night = data['list'][18]
        if time_of_day == 'night':
            now_info_21_morning = data['list'][10]
            now_info_22_day = data['list'][12]
            now_info_23_evening = data['list'][14]
            now_info_24_night = data['list'][16]
        get_weather_all(city)
        txt_name_city.delete(1.0, END)
        txt_name_city.insert(END, f'Вы выбрали город {city}')
        lbl_morning_icon = Label(window, image=morning_icon, borderwidth=0, highlightthickness=0)
        lbl_morning_icon.place(relx=0.1, rely=0.2, anchor='center')
        lbl_day_icon = Label(window, image=day_icon, borderwidth=0, highlightthickness=0)
        lbl_day_icon.place(relx=0.35, rely=0.2, anchor='center')
        lbl_evening_icon = Label(window, image=evening_icon, borderwidth=0, highlightthickness=0)
        lbl_evening_icon.place(relx=0.605, rely=0.2, anchor='center')
        lbl_night_icon = Label(window, image=night_icon, borderwidth=0, highlightthickness=0)
        lbl_night_icon.place(relx=0.855, rely=0.2, anchor='center')
        lbl_morning_2 = Label(window, text='Утро', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_morning_2.place(relx=0.095, rely=0.1275, anchor='center')
        lbl_day_2 = Label(window, text='День', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_day_2.place(relx=0.35, rely=0.1275, anchor='center')
        lbl_evening_2 = Label(window, text='Вечер', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_evening_2.place(relx=0.605, rely=0.1275, anchor='center')
        lbl_night_2 = Label(window, text='Ночь', font=('San Francisco', 14), bg='#6ccccc', fg='#333333')
        lbl_night_2.place(relx=0.855, rely=0.1275, anchor='center')

        info_weather_1_morning = {
            'now_info': now_info_21_morning,
            'time_update': now_info_21_morning['dt_txt'],
            'temp': round((int(now_info_21_morning['main']['temp']) - 273.15), 2),
            'condition': now_info_21_morning['weather'][0]['id'],
            'wind': now_info_21_morning['wind']['speed'],
            'pop': round((now_info_21_morning['pop'] * 100), 2),
            'precip': now_info_21_morning['rain']['3h'] if 'rain' in now_info_21_morning else 0,
            'humidity': now_info_21_morning['main']['humidity'],
            'cloud': now_info_21_morning['clouds']['all'],
            'feelslike': round((int(now_info_21_morning['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_day = {
            'now_info': now_info_22_day,
            'time_update': now_info_22_day['dt_txt'],
            'temp': round((int(now_info_22_day['main']['temp']) - 273.15), 2),
            'condition': now_info_22_day['weather'][0]['id'],
            'wind': now_info_22_day['wind']['speed'],
            'pop': round((now_info_22_day['pop'] * 100), 2),
            'precip': now_info_22_day['rain']['3h'] if 'rain' in now_info_22_day else 0,
            'humidity': now_info_22_day['main']['humidity'],
            'cloud': now_info_22_day['clouds']['all'],
            'feelslike': round((int(now_info_22_day['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_evening = {
            'now_info': now_info_23_evening,
            'time_update': now_info_23_evening['dt_txt'],
            'temp': round((int(now_info_23_evening['main']['temp']) - 273.15), 2),
            'condition': now_info_23_evening['weather'][0]['id'],
            'wind': now_info_23_evening['wind']['speed'],
            'pop': round((now_info_23_evening['pop'] * 100), 2),
            'precip': now_info_23_evening['rain']['3h'] if 'rain' in now_info_23_evening else 0,
            'humidity': now_info_23_evening['main']['humidity'],
            'cloud': now_info_23_evening['clouds']['all'],
            'feelslike': round((int(now_info_23_evening['main']['feels_like']) - 273.15), 2),
        }
        info_weather_1_night = {
            'now_info': now_info_24_night,
            'time_update': now_info_24_night['dt_txt'],
            'temp': round((int(now_info_24_night['main']['temp']) - 273.15), 2),
            'condition': now_info_24_night['weather'][0]['id'],
            'wind': now_info_24_night['wind']['speed'],
            'pop': round((now_info_24_night['pop'] * 100), 2),
            'precip': now_info_24_night['rain']['3h'] if 'rain' in now_info_24_night else 0,
            'humidity': now_info_24_night['main']['humidity'],
            'cloud': now_info_24_night['clouds']['all'],
            'feelslike': round((int(now_info_24_night['main']['feels_like']) - 273.15), 2),
        }
        label_weather_morning_2 = Label(window, borderwidth=0)
        if info_weather_1_morning['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_morning['condition']]
            create_weather_gif(weather_path, label_weather_morning_2)
            label_weather_morning_2.place(relx=0.0585, rely=0.315)
        label_weather_day_2 = Label(window, borderwidth=0)
        if info_weather_1_day['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_day['condition']]
            create_weather_gif(weather_path, label_weather_day_2)
            label_weather_day_2.place(relx=0.315, rely=0.315)
        label_weather_evening_2 = Label(window, borderwidth=0)
        if info_weather_1_evening['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_evening['condition']]
            create_weather_gif(weather_path, label_weather_evening_2)
            label_weather_evening_2.place(relx=0.565, rely=0.315)
        label_weather_night_2 = Label(window, borderwidth=0)
        if info_weather_1_night['condition'] in weather_mapping:
            weather_path = weather_mapping[info_weather_1_night['condition']]
            create_weather_gif(weather_path, label_weather_night_2)
            label_weather_night_2.place(relx=0.815, rely=0.315)
        now_info_know_time = data['list'][0]
        time_update = now_info_know_time['dt_txt']
        date_object = datetime.strptime(info_weather_1_morning["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_morning = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                   bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_morning.place(relx=0.005, rely=0.6175, anchor='w')
        txt_weather_morning.delete(1.0, END)
        txt_weather_morning.insert(END, f'{formatted_date}\n\n'
                                        f'Температура — {info_weather_1_morning["temp"]}°C\n'
                                        f'Скорость ветра — {info_weather_1_morning["wind"]} км/ч\n'
                                        f'Вероятность осадков — {info_weather_1_morning["pop"]} %\n'
                                        f'Осадки за 3 часа — {info_weather_1_morning["precip"]} мм\n'
                                        f'Влажность — {info_weather_1_morning["humidity"]} %\n'
                                        f'Облачность — {info_weather_1_morning["cloud"]} %\n'
                                        f'Ощущается — {info_weather_1_morning["feelslike"]}°C\n')
        txt_weather_morning.tag_add('bold', '1.0', '1.end')
        txt_weather_morning.tag_add('italic', '2.0', 'end')
        txt_weather_morning.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_morning.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_day["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_day = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                               bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_day.place(relx=0.255, rely=0.6175, anchor='w')
        txt_weather_day.delete(1.0, END)
        txt_weather_day.insert(END, f'{formatted_date}\n\n'
                                    f'Температура — {info_weather_1_day["temp"]}°C\n'
                                    f'Скорость ветра — {info_weather_1_day["wind"]} км/ч\n'
                                    f'Вероятность осадков — {info_weather_1_day["pop"]} %\n'
                                    f'Осадки за 3 часа — {info_weather_1_day["precip"]} мм\n'
                                    f'Влажность — {info_weather_1_day["humidity"]} %\n'
                                    f'Облачность — {info_weather_1_day["cloud"]} %\n'
                                    f'Ощущается — {info_weather_1_day["feelslike"]}°C\n')
        txt_weather_day.tag_add('bold', '1.0', '1.end')
        txt_weather_day.tag_add('italic', '2.0', 'end')
        txt_weather_day.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_day.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_evening["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_evening = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                   bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_evening.place(relx=0.505, rely=0.6175, anchor='w')
        txt_weather_evening.delete(1.0, END)
        txt_weather_evening.insert(END, f'{formatted_date}\n\n'
                                        f'Температура — {info_weather_1_evening["temp"]}°C\n'
                                        f'Скорость ветра — {info_weather_1_evening["wind"]} км/ч\n'
                                        f'Вероятность осадков — {info_weather_1_evening["pop"]} %\n'
                                        f'Осадки за 3 часа — {info_weather_1_evening["precip"]} мм\n'
                                        f'Влажность — {info_weather_1_evening["humidity"]} %\n'
                                        f'Облачность — {info_weather_1_evening["cloud"]} %\n'
                                        f'Ощущается — {info_weather_1_evening["feelslike"]}°C\n')
        txt_weather_evening.tag_add('bold', '1.0', '1.end')
        txt_weather_evening.tag_add('italic', '2.0', 'end')
        txt_weather_evening.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_evening.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        date_object = datetime.strptime(info_weather_1_night["time_update"], '%Y-%m-%d %H:%M:%S')
        month_number = date_object.month
        declined_month = decline_month(month_number)
        formatted_date = date_object.strftime(f'%d {declined_month} в %H:%M')
        txt_weather_night = Text(window, font=('San Francisco', 10), wrap="word", height=8.5, width=33,
                                 bg='#6ccccc', fg='#333333', borderwidth=0)
        txt_weather_night.place(relx=0.755, rely=0.6175, anchor='w')
        txt_weather_night.delete(1.0, END)
        txt_weather_night.insert(END, f'{formatted_date}\n\n'
                                      f'Температура — {info_weather_1_night["temp"]}°C\n'
                                      f'Скорость ветра — {info_weather_1_night["wind"]} км/ч\n'
                                      f'Вероятность осадков — {info_weather_1_night["pop"]} %\n'
                                      f'Осадки за 3 часа — {info_weather_1_night["precip"]} мм\n'
                                      f'Влажность — {info_weather_1_night["humidity"]} %\n'
                                      f'Облачность — {info_weather_1_night["cloud"]} %\n'
                                      f'Ощущается — {info_weather_1_night["feelslike"]}°C\n')
        txt_weather_night.tag_add('bold', '1.0', '1.end')
        txt_weather_night.tag_add('italic', '2.0', 'end')
        txt_weather_night.tag_configure('bold', font=('San Francisco', 10, 'bold'))
        txt_weather_night.tag_configure('italic', font=('San Francisco', 8, 'italic'))
        lbl_last_update = Label(window, text=f'Информация была обновлена {time_update}',
                                font=('San Francisco', 12, 'italic'), bg='#6ccccc', fg='#333333')
        lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
        labels_3.extend([txt_name_city, lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2, txt_weather_morning,
                         txt_weather_day, txt_weather_evening, txt_weather_night, lbl_last_update, lbl_morning_icon,
                         lbl_day_icon, lbl_evening_icon, lbl_night_icon])
        labels_weather.extend([label_weather_morning_2, label_weather_day_2,
                               label_weather_evening_2, label_weather_night_2])

    # Кнопка ввода нового города
    def clicked_back():
        global city, labels, labels_2, labels_3, stop_bg, btn_enter_city, lbl_start, btn_enter_city, \
            lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2, txt_city
        stop_bg = False
        update_bg_gif(0)
        if lbl_morning_2:
            lbl_morning_2.destroy()
        if lbl_day_2:
            lbl_day_2.destroy()
        if lbl_evening_2:
            lbl_evening_2.destroy()
        if lbl_night_2:
            lbl_night_2.destroy()
        for label in labels:
            label.destroy()
        for label in labels_2:
            label.destroy()
        for label in labels_3:
            label.destroy()
        for label in labels_weather:
            label.destroy()
        labels = []
        labels_2 = []
        labels_3 = []
        window.update()
        lbl_start = Label(window, text='Введите название города', font=('San Francisco', 22),
                          bg='#6ccccc', fg='#333333')
        lbl_start.place(relx=0.5, rely=0.2, anchor='center')
        lbl_my = Label(window, text='Made by yurokbrat', font=('Montserrat', 10, 'italic'), bg='#6ccccc', fg='#333333')
        lbl_my.place(relx=1, rely=1.005, anchor='se')
        txt_city = ttk.Entry(window, style='Rounded.TEntry', width=50, justify='center')
        txt_city.place(relx=0.5, rely=0.5, anchor='center')
        txt_city.icursor(len(txt_city.get()) // 2)
        btn_enter_city = ttk.Button(window, text='\nВвести\n', command=clicked, style="TButton", width=15)
        btn_enter_city.place(relx=0.5, rely=0.7, anchor='center')
        city = None


display_weather()
window.mainloop()
