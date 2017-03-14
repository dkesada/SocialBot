#! /usr/bin/python
#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes

import sys
import time
import threading
from Queue import Queue
import telepot
import telepot.helper

from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

import googlemaps
from datetime import datetime

import json
import datetime
import db
import steps
import keyboards

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

mapclient = googlemaps.Client(key=sys.argv[1]) #Input the api places key as the first argument when launching
#mapdirections = googlemaps.Client(key=sys.argv[2]) #Input the api directions key as the second argument when launching


# One UserHandler created per chat_id. May be useful for sorting out users
# Handles chat messages depending on its tipe
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg,flavor='chat')
		if content_type == 'text':
			if msg['text'] == "/start":
				db.setStep(chat_id, 0)
			if steps.step(chat_id) == "Init":
				bot.sendMessage(chat_id, 'Share your location', reply_markup=keyboards.markupLocation)
		elif content_type == 'location':
			db.storeLocation(chat_id, msg['location'], msg['date'])
			#thanks = 'Thanks ' + msg['chat']['first_name']
			#bot.sendMessage(chat_id, thanks, reply_markup=markupBack)
			steps.nextStep(chat_id)
			bot.sendMessage(chat_id, 'What are you looking for?', reply_markup=keyboards.inlineEstablishment)			
    
    def on__idle(self, event):
        self.close()
        
			
# One ButtonHandler created per message that has a button pressed.
# There should only be one message from the bot at a time in a chat, so that
# you modify the same message over and over again.
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(ButtonHandler, self).__init__(*args, **kwargs)
        
    def placesNearBy(self, establishmentType, chat_id):
		data = db.getLocation(chat_id)
		latitude = data[0]
		longitude = data[1]
		js = mapclient.places_nearby(location=(latitude, longitude), type=establishmentType, language='es-ES', radius=2000, min_price=0, max_price=4, open_now=True)
		if js["results"] != 'ZERO_RESULTS':
			self.editor.editMessageText('Choose one', reply_markup=keyboards.resultsKeyboard(js))
		else:
			self.editor.editMessageText("There aren't establishment available with this parameters", reply_markup=None)
		    
    def on_callback_query(self, msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		bot.answerCallbackQuery(query_id)

		if query_data == "back":
			stp = steps.stepBack(from_id)	
			if stp != False:
				if stp == "Init":
					bot.sendMessage(from_id, 'Share your location', reply_markup=keyboards.markupLocation)
				elif stp == "Choose Type":
					bot.sendMessage(from_id, 'What are you looking for?', reply_markup=keyboards.inlineEstablishment)
				elif stp == "Choose Establish":
					self.placesNearBy(query_data, from_id)					
		elif steps.step(from_id) == "Choose Type":
			steps.nextStep(from_id)
			self.placesNearBy(query_data, from_id)			
		elif steps.step(from_id) == "Choose Establish":
			steps.nextStep(from_id)
			data = query_data.split(" ")
			lat = data[0]
			lng = data[1]
			bot.sendLocation(from_id,lat,lng)	
			bot.sendMessage(from_id,"Here it is", reply_markup=keyboards.inlineBack)		
            
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
