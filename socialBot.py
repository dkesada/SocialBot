#! /usr/bin/python
#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes

import sys
import time
import threading
from Queue import Queue
import telepot
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

import googlemaps
from datetime import datetime

import json

"""
Utilizando el _nearby despues de enviar la localizacion devuelvo una lista de restaurantes
que cumplen las caracteristicas de la query. Son callback_quey asi que cuando elige uno
le envío la localización. Hay que mirar de mostrarlos de una forma mas agradable y quizas 
en un orden, ya sea valoración, cercania etc. También haabría que enviar las caracteristicas
de los locales

La clave de la api de google la introduzco por consola, para no tenerla publicada en github

He empezado a usar esto para sacar los locales cercanos a la ubicación que te manden:
https://github.com/googlemaps/google-maps-services-python

Aquí está la documentación de las funciones que tiene:
https://googlemaps.github.io/google-maps-services-python/docs/2.4.5/

Documentacion de telepot:
http://telepot.readthedocs.io/en/latest/reference.html

"""

# Readying the google maps client

mapclient = googlemaps.Client(key=sys.argv[1]) #Input the api key as the first argument when launching

locations = {}
# One UserHandler created per chat_id. May be useful for sorting out users
# Handles chat messages depending on its tipe
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)
        
    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg,flavor='chat')
        if content_type == 'text':	
            markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Location', request_location=True)],], resize_keyboard=True)
            bot.sendMessage(chat_id, 'Share your location', reply_markup=markup)
					
        elif content_type == 'location':
			locations[chat_id] = str(msg['location']['latitude']) + " " + str(msg['location']['longitude'])
			
			buttonsInline = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Bar', callback_data='bar')] + [InlineKeyboardButton(text='Cafe', callback_data='cafe')],
					[InlineKeyboardButton(text='Food', callback_data='food')]+ [InlineKeyboardButton(text='Night club', callback_data='night_club')],
					[InlineKeyboardButton(text='Restaurant', callback_data='restaurant')],
               ])
               
			bot.sendMessage(chat_id, 'What are you looking for?', reply_markup=buttonsInline)
    
    def on__idle(self, event):
        self.close()
			
# One ButtonHandler created per message that has a button pressed.
# There should only be one message from the bot at a time in a chat, so that
# you modify the same message over and over again.
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(ButtonHandler, self).__init__(*args, **kwargs)
        
    def placesNearBy(self, establishmentType, chat_id):
        data = []
        data = locations[chat_id].split(" ")
        latitude = data[0]
        longitude = data[1]
        js = mapclient.places_nearby(location=(latitude, longitude), type=establishmentType, language='es-ES', radius=2000, min_price=0, max_price=4, open_now=True)

        keyboardRestaurant= []
        for j in js["results"]:
            loc = "L " + str(j["geometry"]["location"]["lat"]) + " " + str(j["geometry"]["location"]["lng"])
            keyboardRestaurant= keyboardRestaurant + [InlineKeyboardButton(text=j["name"], callback_data=loc)]

        markupRestaurant = InlineKeyboardMarkup(inline_keyboard = [keyboardRestaurant])
        bot.sendMessage(chat_id, 'Choose one', reply_markup=markupRestaurant)
     
		    
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        bot.answerCallbackQuery(query_id)
		
        if query_data[0] == "L":
            data = []
            data = query_data.split(" ")
            bot.sendLocation(from_id, data[0], data[1])
        else:
            self.placesNearBy(query_data, from_id)
            
    def on__idle(self, event):
        self.close()
			
TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=10),
    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=30),
])

bot.message_loop(run_forever='Listening')
