import json
import requests
import telebot
from geopy import geocoders
from translate import Translator
from multiprocessing.context import Process
import schedule
import time


def start_process():
    p1 = Process(target=P_schedule.start_schedule, args=()).start()


class P_schedule():
    def start_schedule():
        schedule.every().day.at("10:00").do(resent_message)

        while True:
            schedule.run_pending()
            time.sleep(1)


def translate_weather(words):
    translator = Translator(to_lang="Russian")
    translation = translator.translate(words)
    return translation


def geo_pos(city):
    geolocator = geocoders.Nominatim(user_agent="telebot")
    latitude = str(geolocator.geocode(city).latitude)
    longitude = str(geolocator.geocode(city).longitude)
    return latitude, longitude


def weather_in_city(latitude, longitude):
    url_weather = f'https://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid=3cbc754faada3a731dd38275eb194770'
    response = requests.get(url_weather)
    json_data = json.loads(response.text)
    dict_weather = dict()
    dict_weather["temp"] = int(json_data["main"]["temp"]) - 273
    weather_on_russian = translate_weather(json_data["weather"][0]["main"])
    if weather_on_russian == "Очистить":
        weather_on_russian = "ни облочка"
    dict_weather["weather"] = weather_on_russian
    return dict_weather


def resent_message():
    for client in clients:
        city = clients[client]
        latitude, longitude = geo_pos(city)
        you_weather = weather_in_city(latitude, longitude)
        bot.send_message(client, f' Температура сейчас {you_weather["temp"]}!'
                                 f' А на небе {you_weather["weather"]}.')


def print_weather(dict_weather, message):
    bot.send_message(message.from_user.id, f' Температура сейчас {dict_weather["temp"]}!'
                                           f' А на небе {dict_weather["weather"]}.')


bot = telebot.TeleBot("5027574826:AAFag0KMdDDpvg6WJa9j5JSgEczmbqsYtQE")

clients = {336065295: "Москва"}


@bot.message_handler(commands=['start', 'help'])
def send_massage(message):
    bot.send_message(message.from_user.id,
                     f'Я Sebastian - бот погоды, приятно познакомитсья, {message.from_user.first_name},'
                     f' Напишите название города, в котором хотите узнать погоду.')


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    city = message.text
    clients[message.from_user.id] = city
    latitude, longitude = geo_pos(city)
    you_weather = weather_in_city(latitude, longitude)
    print_weather(you_weather, message)


if __name__ == '__main__':
    start_process()
    try:
        bot.infinity_polling()
    except:
        pass
