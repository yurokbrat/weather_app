import tkinter

import requests
from tkinter import *
from PIL import Image, ImageTk, ImageSequence
from tkinter import ttk, font, Text, END
from ttkthemes import ThemedTk, ThemedStyle
from time import strftime
from datetime import datetime

# Создание окна приложения
window = ThemedTk(theme='claim')
window.title('Прогноз погоды')
window.geometry('800x600')
# window.wm_resizable(0, 0)
window.iconbitmap('E:\\программирование\\weather\\weathers_gif\\icon.ico')
info_weather = {}
bg_image_2 = None
city = None
lbl_morning_2 = None
lbl_day_2 = None
lbl_evening_2 = None
lbl_night_2 = None
labels = []

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


def get_weather_all(city):
    global data
    base = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&appid=a0e0c0ffae85a246ab2fefe8634c1aff'
    result = requests.get(base)
    data = result.json()


# Настройка приложения
def display_weather():
    global lbl_start, city, txt_city, lbl_morning, lbl_day, lbl_evening, lbl_night
    bg_image = Image.open('E:\\программирование\\weather\\weathers_gif\\background.gif')
    bg_start_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(bg_image)]
    anime_image = Image.open('E:\\программирование\\weather\\weathers_gif\\girl.gif')
    anime_girl_image = [ImageTk.PhotoImage(frame) for frame in ImageSequence.Iterator(anime_image)]

    def update_girl_gif(k):
        frame = anime_girl_image[k]
        k = (k + 1) % len(anime_girl_image)
        label_girl_start.configure(image=frame)
        window.after(80, update_girl_gif, k)

    def update_bg_gif(k):
        frame = bg_start_image[k]
        k = (k + 1) % len(bg_start_image)
        label_back_start.configure(image=frame)
        window.after(60, update_bg_gif, k)

    style = ttk.Style()
    style.configure('Tbutton', padding=5, font=('San Francisco', 12), background='#3498db', foreground='white')
    style.configure('Rounded.TEntry', padding=5, font=('San Francisco', 22), relief='flat',
                    borderwidth=55, background='#99FFFF', focuscolor='#003366', fieldbackground='white')
    label_back_start = Label(window)
    label_back_start.place(relwidth=1, relheight=1)
    update_bg_gif(0)
    label_girl_start = Label(window, borderwidth=0)
    label_girl_start.place(relx=-0.05, rely=0.843)
    update_girl_gif(0)

    lbl_start = Label(window, text='Введите название города', font=('San Francisco', 22),
                      bg='#99FFFF', fg='#333333')
    lbl_start.place(relx=0.5, rely=0.24, anchor='center')
    lbl_my = Label(window, text='Made by yurokbrat', font=('Montserrat', 10, 'italic'), bg='#99FFFF', fg='#333333')
    lbl_my.place(relx=1, rely=1.005, anchor='se')
    txt_city = ttk.Entry(window, style='Rounded.TEntry', width=50, justify='center')
    txt_city.place(relx=0.5, rely=0.5, anchor='center')
    txt_city.icursor(len(txt_city.get()) // 2)
    lbl_morning = None
    lbl_day = None
    lbl_evening = None
    lbl_night = None

    def clicked():
        global city, labels,txt_city, txt_weather, txt_name_city, lbl_morning, lbl_day, lbl_evening, lbl_night

        def show_time():
            string = strftime('%H:%M:%S')
            label_time.config(text=string)
            label_time.after(1000, show_time)

        if city is None:
            city = txt_city.get()
        get_weather_all(city)
        label_time = tkinter.Label(window, font=('calibri', 15, 'bold'), background='#99FFFF', foreground='#333333')
        label_time.place(relx=0.025, rely=0.05, anchor='w')
        show_time()
        lbl_morning = Label(window, text='Утро', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_morning.place(relx=0.105, rely=0.1775, anchor='center')
        lbl_day = Label(window, text='День', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_day.place(relx=0.355, rely=0.1775, anchor='center')
        lbl_evening = Label(window, text='Вечер', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_evening.place(relx=0.605, rely=0.1775, anchor='center')
        lbl_night = Label(window, text='Ночь', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_night.place(relx=0.855, rely=0.1775, anchor='center')
        lbl_start.place_forget()
        txt_city.place_forget()
        labels.append(label_time)
        if time_of_day == 'morning':
            now_info = data['list'][0]
            info_weather_morning = {
                'now_info': now_info,
                'time_update': now_info['dt_txt'],
                'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
                'wind': now_info['wind']['speed'],
                'pop': round((now_info['pop'] * 100), 2),
                'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                'humidity': now_info['main']['humidity'],
                'cloud': now_info['clouds']['all'],
                'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
            }

            txt_weather_morning = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                       bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_morning.delete(1.0, END)
            txt_weather_morning.insert(END, f'{info_weather_morning["time_update"]}\n'
                                            f'Температура — {info_weather_morning["temp"]}°C,\n'
                                            f'Скорость ветра — {info_weather_morning["wind"]} км/ч,\n'
                                            f'Вероятность дождя — {info_weather_morning["pop"]} %,\n'
                                            f'Влажность — {info_weather_morning["humidity"]} %,\n'
                                            f'Облачность — {info_weather_morning["cloud"]} %,\n'
                                            f'Ощущается как — {info_weather_morning["feelslike"]}°C\n')
            txt_weather_morning.place(relx=0.005, rely=0.6, anchor='w')
            txt_weather_day = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_day.destroy()
            txt_weather_day.place(relx=0.255, rely=0.6, anchor='w')
            txt_weather_day.delete(1.0, END)
            txt_weather_day.insert(END, f'{info_weather_day["time_update"]}\n'
                                        f'Температура — {info_weather_day["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_day["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_day["pop"]} %,\n'
                                        f'Влажность — {info_weather_day["humidity"]} %,\n'
                                        f'Облачность — {info_weather_day["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_day["feelslike"]}°C\n')
            txt_weather_evening = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                       bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_evening.place(relx=0.505, rely=0.6, anchor='w')
            txt_weather_evening.delete(1.0, END)
            txt_weather_evening.insert(END, f'{info_weather_evening["time_update"]}\n'
                                            f'Температура — {info_weather_evening["temp"]}°C,\n'
                                            f'Скорость ветра — {info_weather_evening["wind"]} км/ч,\n'
                                            f'Вероятность дождя — {info_weather_evening["pop"]} %,\n'
                                            f'Влажность — {info_weather_evening["humidity"]} %,\n'
                                            f'Облачность — {info_weather_evening["cloud"]} %,\n'
                                            f'Ощущается как — {info_weather_evening["feelslike"]}°C\n')
            txt_weather_night = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                     bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_night.place(relx=0.755, rely=0.6, anchor='w')
            txt_weather_night.delete(1.0, END)
            txt_weather_night.insert(END, f'{info_weather_night["time_update"]}\n'
                                          f'Температура — {info_weather_night["temp"]}°C,\n'
                                          f'Скорость ветра — {info_weather_night["wind"]} км/ч,\n'
                                          f'Вероятность дождя — {info_weather_night["pop"]} %,\n'
                                          f'Влажность — {info_weather_night["humidity"]} %,\n'
                                          f'Облачность — {info_weather_night["cloud"]} %,\n'
                                          f'Ощущается как — {info_weather_night["feelslike"]}°C\n')
            lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_morning["time_update"]}',
                                    font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
            lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
            labels.extend([label_time, lbl_morning, lbl_day, lbl_evening, lbl_night,
                           txt_weather_morning, txt_weather_day, txt_weather_evening,
                           txt_weather_night, lbl_last_update])

        if time_of_day == 'day':
            lbl_morning.place_forget()
            lbl_day.place(relx=0.125, rely=0.1775, anchor='center')
            lbl_evening.place(relx=0.475, rely=0.1775, anchor='center')
            lbl_night.place(relx=0.825, rely=0.1775, anchor='center')
            now_info = data['list'][0]
            info_weather_day = {
                'now_info': now_info,
                'time_update': now_info['dt_txt'],
                'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
                'wind': now_info['wind']['speed'],
                'pop': round((now_info['pop'] * 100), 2),
                'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                'humidity': now_info['main']['humidity'],
                'cloud': now_info['clouds']['all'],
                'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
            }

            txt_weather_day = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_day.place(relx=0.025, rely=0.6, anchor='w')
            txt_weather_day.delete(1.0, END)
            txt_weather_day.insert(END, f'{info_weather_day["time_update"]}\n'
                                        f'Температура — {info_weather_day["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_day["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_day["pop"]} %,\n'
                                        f'Кол-во осадков за 3 часа — {info_weather_day["precip"]} мм,\n'
                                        f'Влажность — {info_weather_day["humidity"]} %,\n'
                                        f'Облачность — {info_weather_day["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_day["feelslike"]}°C\n')
            txt_weather_evening = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                       bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_evening.place(relx=0.375, rely=0.6, anchor='w')
            txt_weather_evening.delete(1.0, END)
            txt_weather_evening.insert(END, f'{info_weather_evening["time_update"]}\n'
                                            f'Температура — {info_weather_evening["temp"]}°C,\n'
                                            f'Скорость ветра — {info_weather_evening["wind"]} км/ч,\n'
                                            f'Вероятность дождя — {info_weather_evening["pop"]} %,\n'
                                            f'Кол-во осадков за 3 часа — {info_weather_evening["precip"]} мм,\n'
                                            f'Влажность — {info_weather_evening["humidity"]} %,\n'
                                            f'Облачность — {info_weather_evening["cloud"]} %,\n'
                                            f'Ощущается как — {info_weather_evening["feelslike"]}°C\n')
            txt_weather_night = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                     bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_night.place(relx=0.725, rely=0.6, anchor='w')
            txt_weather_night.delete(1.0, END)
            txt_weather_night.insert(END, f'{info_weather_night["time_update"]}\n'
                                          f'Температура — {info_weather_night["temp"]}°C,\n'
                                          f'Скорость ветра — {info_weather_night["wind"]} км/ч,\n'
                                          f'Вероятность дождя — {info_weather_night["pop"]} %,\n'
                                          f'Кол-во осадков за 3 часа — {info_weather_night["precip"]} мм,\n'
                                          f'Влажность — {info_weather_night["humidity"]} %,\n'
                                          f'Облачность — {info_weather_night["cloud"]} %,\n'
                                          f'Ощущается как — {info_weather_night["feelslike"]}°C\n')
            lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_day["time_update"]}',
                                    font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
            lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
            labels.extend([lbl_day, lbl_evening, lbl_night, txt_weather_day, txt_weather_evening,
                           txt_weather_night, lbl_last_update])

        if time_of_day == 'evening':
            lbl_morning.place_forget()
            lbl_day.place_forget()
            lbl_evening.place(relx=0.225, rely=0.1775, anchor='center')
            lbl_night.place(relx=0.775, rely=0.1775, anchor='center')
            now_info = data['list'][0]
            info_weather_evening = {
                'now_info': now_info,
                'time_update': now_info['dt_txt'],
                'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                'condition': now_info['weather'][0]['main'],
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
                'condition': now_info['weather'][0]['main'],
                'wind': now_info['wind']['speed'],
                'pop': round((now_info['pop'] * 100), 2),
                'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                'humidity': now_info['main']['humidity'],
                'cloud': now_info['clouds']['all'],
                'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
            }
            txt_weather_evening = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                       bg='#99FFFF', fg='#333333', borderwidth=0, state="normal")
            txt_weather_evening.delete(1.0, END)
            txt_weather_evening.place(relx=0.125, rely=0.6, anchor='w')
            txt_weather_evening.insert(END, f'{info_weather_evening["time_update"]}\n'
                                            f'Температура — {info_weather_evening["temp"]}°C,\n'
                                            f'Скорость ветра — {info_weather_evening["wind"]} км/ч,\n'
                                            f'Вероятность дождя — {info_weather_evening["pop"]} %,\n'
                                            f'Кол-во осадков за 3 часа — {info_weather_evening["precip"]} мм,\n'
                                            f'Влажность — {info_weather_evening["humidity"]} %,\n'
                                            f'Облачность — {info_weather_evening["cloud"]} %,\n'
                                            f'Ощущается как — {info_weather_evening["feelslike"]}°C\n')
            txt_weather_night = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                     bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_night.place(relx=0.665, rely=0.6, anchor='w')
            txt_weather_night.delete(1.0, END)
            txt_weather_night.insert(END, f'{info_weather_night["time_update"]}\n'
                                          f'Температура — {info_weather_night["temp"]}°C,\n'
                                          f'Скорость ветра — {info_weather_night["wind"]} км/ч,\n'
                                          f'Вероятность дождя — {info_weather_night["pop"]} %,\n'
                                          f'Кол-во осадков за 3 часа — {info_weather_night["precip"]} мм,\n'
                                          f'Влажность — {info_weather_night["humidity"]} %,\n'
                                          f'Облачность — {info_weather_night["cloud"]} %,\n'
                                          f'Ощущается как — {info_weather_night["feelslike"]}°C\n')
            lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_evening["time_update"]}',
                                    font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
            lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
            labels.extend([lbl_evening, lbl_night, txt_weather_evening, txt_weather_night, lbl_last_update])

        if time_of_day == 'night':
            lbl_morning.place_forget()
            lbl_day.place_forget()
            lbl_evening.place_forget()
            lbl_night.place(relx=0.5, rely=0.1775, anchor='center')
            now_info = data['list'][0]
            info_weather_night = {
                'now_info': now_info,
                'time_update': now_info['dt_txt'],
                'temp': round((int(now_info['main']['temp']) - 273.15), 2),
                'condition': now_info['weather'][0]['main'],
                'wind': now_info['wind']['speed'],
                'pop': round((now_info['pop'] * 100), 2),
                'precip': now_info['rain']['3h'] if 'rain' in now_info else 0,
                'humidity': now_info['main']['humidity'],
                'cloud': now_info['clouds']['all'],
                'feelslike': round((int(now_info['main']['feels_like']) - 273.15), 2),
            }
            txt_weather_night = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=33,
                                     bg='#99FFFF', fg='#333333', borderwidth=0)
            txt_weather_night.place(relx=0.395, rely=0.6, anchor='w')
            txt_weather_night.delete(1.0, END)
            txt_weather_night.insert(END, f'{info_weather_night["time_update"]}\n'
                                          f'Температура — {info_weather_night["temp"]}°C,\n'
                                          f'Скорость ветра — {info_weather_night["wind"]} км/ч,\n'
                                          f'Вероятность дождя — {info_weather_night["pop"]} %,\n'
                                          f'Кол-во осадков за 3 часа — {info_weather_night["precip"]} мм,\n'
                                          f'Влажность — {info_weather_night["humidity"]} %,\n'
                                          f'Облачность — {info_weather_night["cloud"]} %,\n'
                                          f'Ощущается как — {info_weather_night["feelslike"]}°C\n')
            lbl_last_update = Label(window, text=f'Информация была обновлена {info_weather_night["time_update"]}',
                                    font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
            lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')
            labels.extend([lbl_night, txt_weather_night, lbl_last_update])

        txt_name_city = Text(window, font=('San Francisco', 18,), wrap="word", height=1,
                             width=30, bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_name_city.tag_configure('center', justify='center')
        txt_name_city.tag_add('center', '1.0', 'end')
        txt_name_city.place(relx=0.575, rely=0.1225, anchor='center')
        txt_name_city.insert(END, f'Вы выбрали город {city}')
        btn_enter_city.place_forget()
        btn_enter_city_first_day = ttk.Button(window, text='\nВвести новый город\n', command=clicked_back,
                                              style="TButton", width=25)
        btn_enter_city_first_day.place(relx=0.15, rely=0.825, anchor='center')
        btn_enter_city_second_day = ttk.Button(window, text='\nПрогноз на завтра\n', command=clicked_1_day,
                                               style="TButton",
                                               width=25)
        btn_enter_city_second_day.place(relx=0.5, rely=0.825, anchor='center')
        btn_enter_city_third_day = ttk.Button(window, text='\nПрогноз на послезавтра\n', command=clicked_2_day,
                                              style="TButton", width=25)
        btn_enter_city_third_day.place(relx=0.85, rely=0.825, anchor='center')
        labels.extend([txt_name_city,btn_enter_city_first_day,btn_enter_city_second_day,btn_enter_city_third_day])
    btn_enter_city = ttk.Button(window, text='\nВвести\n', command=clicked, style="TButton", width=15)
    btn_enter_city.place(relx=0.5, rely=0.7, anchor='center')
    def clicked_1_day():
        global city, lbl_morning, lbl_day, lbl_evening, lbl_night, lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2
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
        lbl_morning_2 = Label(window, text='Утро', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_morning_2.place(relx=0.105, rely=0.1775, anchor='center')
        lbl_day_2 = Label(window, text='День', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_day_2.place(relx=0.355, rely=0.1775, anchor='center')
        lbl_evening_2 = Label(window, text='Вечер', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_evening_2.place(relx=0.605, rely=0.1775, anchor='center')
        lbl_night_2 = Label(window, text='Ночь', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_night_2.place(relx=0.855, rely=0.1775, anchor='center')

        info_weather_1_morning = {
            'now_info': now_info_11_morning,
            'time_update': now_info_11_morning['dt_txt'],
            'temp': round((int(now_info_11_morning['main']['temp']) - 273.15), 2),
            'condition': now_info_11_morning['weather'][0]['main'],
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
            'condition': now_info_12_day['weather'][0]['main'],
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
            'condition': now_info_13_evening['weather'][0]['main'],
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
            'condition': now_info_14_night['weather'][0]['main'],
            'wind': now_info_14_night['wind']['speed'],
            'pop': round((now_info_14_night['pop'] * 100), 2),
            'precip': now_info_14_night['rain']['3h'] if 'rain' in now_info_14_night else 0,
            'humidity': now_info_14_night['main']['humidity'],
            'cloud': now_info_14_night['clouds']['all'],
            'feelslike': round((int(now_info_14_night['main']['feels_like']) - 273.15), 2),
        }
        txt_weather_morning = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_morning.place(relx=0.005, rely=0.6, anchor='w')
        txt_weather_morning.delete(1.0, END)
        txt_weather_morning.insert(END, f'{info_weather_1_morning["time_update"]}\n'
                                        f'Температура — {info_weather_1_morning["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_1_morning["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_1_morning["pop"]} %,\n'
                                        f'Влажность — {info_weather_1_morning["humidity"]} %,\n'
                                        f'Облачность — {info_weather_1_morning["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_1_morning["feelslike"]}°C\n')
        txt_weather_day_1 = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                 bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_day_1.place(relx=0.255, rely=0.6, anchor='w')
        txt_weather_day_1.delete(1.0, END)
        txt_weather_day_1.insert(END, f'{info_weather_1_day["time_update"]}\n'
                                      f'Температура — {info_weather_1_day["temp"]}°C,\n'
                                      f'Скорость ветра — {info_weather_1_day["wind"]} км/ч,\n'
                                      f'Вероятность дождя — {info_weather_1_day["pop"]} %,\n'
                                      f'Влажность — {info_weather_1_day["humidity"]} %,\n'
                                      f'Облачность — {info_weather_1_day["cloud"]} %,\n'
                                      f'Ощущается как — {info_weather_1_day["feelslike"]}°C\n')
        txt_weather_evening_1 = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                     bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_evening_1.place(relx=0.505, rely=0.6, anchor='w')
        txt_weather_evening_1.delete(1.0, END)
        txt_weather_evening_1.insert(END, f'{info_weather_1_evening["time_update"]}\n'
                                          f'Температура — {info_weather_1_evening["temp"]}°C,\n'
                                          f'Скорость ветра — {info_weather_1_evening["wind"]} км/ч,\n'
                                          f'Вероятность дождя — {info_weather_1_evening["pop"]} %,\n'
                                          f'Влажность — {info_weather_1_evening["humidity"]} %,\n'
                                          f'Облачность — {info_weather_1_evening["cloud"]} %,\n'
                                          f'Ощущается как — {info_weather_1_evening["feelslike"]}°C\n')
        txt_weather_night_1 = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_night_1.place(relx=0.755, rely=0.6, anchor='w')
        txt_weather_night_1.delete(1.0, END)
        txt_weather_night_1.insert(END, f'{info_weather_1_night["time_update"]}\n'
                                        f'Температура — {info_weather_1_night["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_1_night["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_1_night["pop"]} %,\n'
                                        f'Влажность — {info_weather_1_night["humidity"]} %,\n'
                                        f'Облачность — {info_weather_1_night["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_1_night["feelslike"]}°C\n')
        lbl_last_update = Label(window, text=f'Информация была обновлена {time_update}',
                                font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
        lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')

    def clicked_2_day():
        global city, lbl_morning, lbl_day, lbl_evening, lbl_night, lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2, txt_weather_morning
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
        lbl_morning_2 = Label(window, text='Утро', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_morning_2.place(relx=0.105, rely=0.1775, anchor='center')
        lbl_day_2 = Label(window, text='День', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_day_2.place(relx=0.355, rely=0.1775, anchor='center')
        lbl_evening_2 = Label(window, text='Вечер', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_evening_2.place(relx=0.605, rely=0.1775, anchor='center')
        lbl_night_2 = Label(window, text='Ночь', font=('San Francisco', 14), bg='#99FFFF', fg='#333333')
        lbl_night_2.place(relx=0.855, rely=0.1775, anchor='center')

        info_weather_1_morning = {
            'now_info': now_info_21_morning,
            'time_update': now_info_21_morning['dt_txt'],
            'temp': round((int(now_info_21_morning['main']['temp']) - 273.15), 2),
            'condition': now_info_21_morning['weather'][0]['main'],
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
            'condition': now_info_22_day['weather'][0]['main'],
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
            'condition': now_info_23_evening['weather'][0]['main'],
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
            'condition': now_info_24_night['weather'][0]['main'],
            'wind': now_info_24_night['wind']['speed'],
            'pop': round((now_info_24_night['pop'] * 100), 2),
            'precip': now_info_24_night['rain']['3h'] if 'rain' in now_info_24_night else 0,
            'humidity': now_info_24_night['main']['humidity'],
            'cloud': now_info_24_night['clouds']['all'],
            'feelslike': round((int(now_info_24_night['main']['feels_like']) - 273.15), 2),
        }
        now_info_know_time = data['list'][0]
        time_update = now_info_know_time['dt_txt']
        txt_weather_morning = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_morning.place(relx=0.005, rely=0.6, anchor='w')
        txt_weather_morning.delete(1.0, END)
        txt_weather_morning.insert(END, f'{info_weather_1_morning["time_update"]}\n'
                                        f'Температура — {info_weather_1_morning["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_1_morning["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_1_morning["pop"]} %,\n'
                                        f'Влажность — {info_weather_1_morning["humidity"]} %,\n'
                                        f'Облачность — {info_weather_1_morning["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_1_morning["feelslike"]}°C\n')
        txt_weather_day = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                               bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_day.place(relx=0.255, rely=0.6, anchor='w')
        txt_weather_day.delete(1.0, END)
        txt_weather_day.insert(END, f'{info_weather_1_day["time_update"]}\n'
                                    f'Температура — {info_weather_1_day["temp"]}°C,\n'
                                    f'Скорость ветра — {info_weather_1_day["wind"]} км/ч,\n'
                                    f'Вероятность дождя — {info_weather_1_day["pop"]} %,\n'
                                    f'Влажность — {info_weather_1_day["humidity"]} %,\n'
                                    f'Облачность — {info_weather_1_day["cloud"]} %,\n'
                                    f'Ощущается как — {info_weather_1_day["feelslike"]}°C\n')
        txt_weather_evening = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                   bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_evening.place(relx=0.505, rely=0.6, anchor='w')
        txt_weather_evening.delete(1.0, END)
        txt_weather_evening.insert(END, f'{info_weather_1_evening["time_update"]}\n'
                                        f'Температура — {info_weather_1_evening["temp"]}°C,\n'
                                        f'Скорость ветра — {info_weather_1_evening["wind"]} км/ч,\n'
                                        f'Вероятность дождя — {info_weather_1_evening["pop"]} %,\n'
                                        f'Влажность — {info_weather_1_evening["humidity"]} %,\n'
                                        f'Облачность — {info_weather_1_evening["cloud"]} %,\n'
                                        f'Ощущается как — {info_weather_1_evening["feelslike"]}°C\n')
        txt_weather_night = Text(window, font=('San Francisco', 10, 'italic'), wrap="word", height=8.5, width=30,
                                 bg='#99FFFF', fg='#333333', borderwidth=0)
        txt_weather_night.place(relx=0.755, rely=0.6, anchor='w')
        txt_weather_night.delete(1.0, END)
        txt_weather_night.insert(END, f'{info_weather_1_night["time_update"]}\n'
                                      f'Температура — {info_weather_1_night["temp"]}°C,\n'
                                      f'Скорость ветра — {info_weather_1_night["wind"]} км/ч,\n'
                                      f'Вероятность дождя — {info_weather_1_night["pop"]} %,\n'
                                      f'Влажность — {info_weather_1_night["humidity"]} %,\n'
                                      f'Облачность — {info_weather_1_night["cloud"]} %,\n'
                                      f'Ощущается как — {info_weather_1_night["feelslike"]}°C\n')
        lbl_last_update = Label(window, text=f'Информация была обновлена {time_update}',
                                font=('San Francisco', 12, 'italic'), bg='#99FFFF', fg='#333333')
        lbl_last_update.place(relx=0.5, rely=0.9825, anchor='center')

    def clicked_back():
        global city, labels, btn_enter_city, lbl_morning_2, lbl_day_2, lbl_evening_2, lbl_night_2,txt_city
        if lbl_morning_2:
            lbl_morning_2.place_forget()
        if lbl_day_2:
            lbl_day_2.place_forget()
        if lbl_evening_2:
            lbl_evening_2.place_forget()
        if lbl_night_2:
            lbl_night_2.place_forget()
        print(labels)
        for label in labels:
            label.destroy()
        labels = []
        print(labels)
        window.update()
        lbl_start = Label(window, text='Введите название города', font=('San Francisco', 22),
                          bg='#99FFFF', fg='#333333')
        lbl_start.place(relx=0.5, rely=0.24, anchor='center')
        lbl_my = Label(window, text='Made by yurokbrat', font=('Montserrat', 10, 'italic'), bg='#99FFFF', fg='#333333')
        lbl_my.place(relx=1, rely=1.005, anchor='se')
        txt_city = ttk.Entry(window, style='Rounded.TEntry', width=50, justify='center')
        txt_city.place(relx=0.5, rely=0.5, anchor='center')
        txt_city.icursor(len(txt_city.get()) // 2)
        btn_enter_city = ttk.Button(window, text='\nВвести\n', command=clicked, style="TButton", width=15)
        btn_enter_city.place(relx=0.5, rely=0.7, anchor='center')
        city = None

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
