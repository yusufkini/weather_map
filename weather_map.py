from tkinter import *
from tkinter import messagebox
import requests
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
import numpy as np
from datetime import datetime

currentDateAndTime = datetime.now()


print(f"{currentDateAndTime.day}/{currentDateAndTime.month}/{currentDateAndTime.day}-"
      f"{currentDateAndTime.hour}:{currentDateAndTime.minute}:{currentDateAndTime.second}")

api_key = ""
city = "Bandırma, TR"
lat = "40.3522"
lon = "27.9767"
url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
url2 = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}"
PATH = ""
weather_image = [PATH+"sun.png", PATH+"storm.png", PATH+"snowflake.png",
                 PATH+"raining.png", PATH+"cloudy.png", PATH+"clouds.png"]

weatherTempList = []
def conversion_kelvin_to_celcius(kelvin):
    # Convert Kelvin to Celcius: 1 Kelvin = -272.15 Celcius
    return int(kelvin - 273.15)
def fetch_url_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error",f"Error fetching data: {e}")
        return None
def get_today_weather_infos(url):
    data = fetch_url_data(url)
    if data:
        temp_C = conversion_kelvin_to_celcius(data["main"]["temp"])
        feels_temp = conversion_kelvin_to_celcius(data["main"]["feels_like"])
        weather_status = data["weather"][0]["description"]
        pressure = int(data["main"]["pressure"])
        humidity = int(data["main"]["humidity"])
        visibility = int(data["visibility"])
        wind_speed = int(data["wind"]["speed"])
        return temp_C,feels_temp,weather_status,pressure,humidity,visibility,wind_speed
    else:
        return None
def bring_4days_weathers_infos(url):
    global weatherTempList
    i = 0
    j = 1
    temp_list_day_1 = []
    temp_list_day_2 = []
    temp_list_day_3 = []
    temp_list_day_4 = []
    weather_status_list = []
    data = fetch_url_data(url)
    #Convert Kelvin to Celcius - 1K = -272.15 Celcius

    for item in data["list"]:
        schedule = item['dt_txt']
        # Split the time into date and hour [2018-04-15 06:00:00]
        next_dates, hour = schedule.split(' ')

        # Stores the current date and prints it once
        year, month, day = next_dates.split('-')
        if i == 0:
            current_day = day,month,year
        temperature = int(float(item["main"]["temp"]) - 272.15)
        weatherTempList.append(temperature)
        weather_status = item["weather"][0]["description"]
        weather_status_list.append(weather_status)
        #print(f"{day}.{month}.{year} - {hour}: {temperature}, Weather Status: {weather_status}")
        i += 1
        if i % 10 == 0:
            j += 1

        if 0 <= i and i <= 9:
            temp_list_day_1.append(temperature)
        elif 10 <= i and i <= 19:
            temp_list_day_2.append(temperature)
        elif 20 <= i and i <= 29:
            temp_list_day_3.append(temperature)
        elif 30 <= i and i <= 39:
            temp_list_day_4.append(temperature)

    day1_maxTemp = max(temp_list_day_1)
    day2_maxTemp = max(temp_list_day_2)
    day3_maxTemp = max(temp_list_day_3)
    day4_maxTemp = max(temp_list_day_4)

    day1_minTemp = min(temp_list_day_1)
    day2_minTemp = min(temp_list_day_2)
    day3_minTemp = min(temp_list_day_3)
    day4_minTemp = min(temp_list_day_4)

    max_values = [day1_maxTemp, day2_maxTemp, day3_maxTemp, day4_maxTemp]
    min_values = [day1_minTemp,day2_minTemp,day3_minTemp,day4_minTemp]

    return max_values,min_values,current_day,weather_status_list

def draw_plot():
    my_figure = plt.figure(figsize=(4,2.5),dpi=100)
    my_axes = my_figure.add_axes([0.2,0.2,0.7,0.7])
    my_axes.plot(weatherTempList, "y-*")
    my_axes.set_xlabel("Data Numbers (1 day has 10 data)")
    my_axes.set_ylabel("Temperature")
    my_axes.set_title("4 Days Temperature Graph")

    # creating the Tkinter canvas
    # containing the Matplotlib figure
    canvas = FigureCanvasTkAgg(my_figure,master=window)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().place(x=20, y=260)

def show_days_state(date,maxTemp,minTemp,y):
    days_state_label = Label(text=f"{date},           "
                                  f"{maxTemp} / {minTemp}°C\n",bg=BACK_GROUND,font=DEFAULT_FONT,pady=20)
    days_state_label.place(x=550,y=65+y)

def setImage(weather_image):
    return ImageTk.PhotoImage(Image.open(weather_image))

forecast_max_temp_list, forecast_min_temp_list, current_day_info,weather_status_list = bring_4days_weathers_infos(url2)
weather_infos_list = get_today_weather_infos(url)

BACK_GROUND = "white"
DEFAULT_FONT = ("Arial",14,"normal")
global_day = f"{currentDateAndTime.day} / "+f"{currentDateAndTime.month} / "+f"{currentDateAndTime.year}"
next_day = int(currentDateAndTime.day) + 1
time_of_Turkiye = f"{currentDateAndTime.hour}:" + f"{currentDateAndTime.minute}"

default_Temperature = weather_infos_list[0]
feels_temp = weather_infos_list[1]
weather_status = weather_infos_list[2]
weather_preassure = weather_infos_list[3]
weather_humidity = weather_infos_list[4]
weather_visibility = weather_infos_list[5]
wind_speed = weather_infos_list[6]

window = Tk()
window.title("Weather Map")
window.minsize(width=900,height=600)
window.config(pady=20,bg=BACK_GROUND)

if weather_status == "clear sky":
    image = setImage(weather_image[0])
    image_label = Label(image=image, bg=BACK_GROUND)
    image_label.place(x=20, y=60)
elif weather_status == "light rain":
    image = setImage(weather_image[3])
    image_label = Label(image=image, bg=BACK_GROUND)
    image_label.place(x=20, y=60)
elif weather_status == "broken clouds":
    image = setImage(weather_image[4])
    image_label = Label(image=image, bg=BACK_GROUND)
    image_label.place(x=20, y=60)
elif weather_status == "scattered clouds":
    image = setImage(weather_image[5])
    image_label = Label(image=image, bg=BACK_GROUND)
    image_label.place(x=20, y=60)


title_label1 = Label(text=f"{global_day}, {time_of_Turkiye}", font=("Arial",9,"normal"), bg=BACK_GROUND)
title_label1.place(x=20,y=10)

title_label2 = Label(text="Bandirma, Balikesir, Turkiye", font=DEFAULT_FONT, bg=BACK_GROUND)
title_label2.place(x=20,y=28)

temperature_label = Label(text=f"{default_Temperature}°C",font=("Arial",24,"normal"), bg=BACK_GROUND)
temperature_label.place(x=85,y=67)

brief_info_label1 = Label(text=f"Feels like: {feels_temp}°C",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label1.place(x=20, y= 120)

brief_info_label2 = Label(text=f"Weather Status: {weather_status}",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label2.place(x=180, y= 120)

brief_info_label3 = Label(text=f"Humidity: %{weather_humidity}",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label3.place(x=20, y= 160)

brief_info_label4 = Label(text=f"Preassure: {weather_preassure}hPa",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label4.place(x=20, y= 140)

brief_info_label5 = Label(text=f"Visibility: {weather_visibility}km",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label5.place(x=180, y= 140)

brief_info_label6 = Label(text=f"Wind Speed: {wind_speed}m/s",font=("Arial",10,"normal"), bg=BACK_GROUND)
brief_info_label6.place(x=180, y= 160)

title_label3 = Label(text="4 Day Forecast",font=("Arial",20,"normal"),bg=BACK_GROUND)
title_label3.place(x=550, y=28)

y_coord = 0
y_coord2 = 0
y_coords = [0, 60, 120, 180]
j = 1
for i in range(4):
    show_days_state(f"{currentDateAndTime.day + j} / {currentDateAndTime.month} / {currentDateAndTime.year}",
                    forecast_max_temp_list[i], forecast_min_temp_list[i],
                    y=y_coord)
    y_coord += 60
    j +=1


draw_plot()
window.mainloop()