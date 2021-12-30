import json
import requests
import telebot
from geopy import geocoders


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
    dict_weather["weather"] = json_data["weather"][0]["main"]
    return dict_weather


def print_weather(dict_weather, message):
    bot.send_message(message.from_user.id, f' Температура сейчас {dict_weather["temp"]}!'
                                           f' А на небе {dict_weather["weather"]}.')


bot = telebot.TeleBot("5027574826:AAFag0KMdDDpvg6WJa9j5JSgEczmbqsYtQE")


@bot.message_handler(commands=['start', 'help'])
def send_massage(message):
    bot.reply_to(message, f'Я Sebastian - бот погоды, приятно познакомитсья, {message.from_user.first_name},'
                          f' Напишите название города, в котором хотите узнать погоду.')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    city = message.text
    latitude, longitude = geo_pos(city)
    you_weather = weather_in_city(latitude, longitude)
    print_weather(you_weather, message)


bot.infinity_polling()
