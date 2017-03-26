#! /usr/bin/python
#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes

import sys
import time
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
				steps.saveStep(chat_id, 0)
			if steps.step(steps.getStep(chat_id)) == "Init":
				bot.sendMessage(chat_id, 'Share your location', reply_markup=keyboards.markupLocation)
		elif content_type == 'location':
			db.storeLocation(chat_id, msg['location'], msg['date'])
			state = steps.getStep(chat_id)
			steps.saveStep(chat_id, steps.nextStep(state))
			bot.sendMessage(chat_id, 'What are you looking for?', reply_markup=keyboards.inlineEstablishment)
		elif content_type == 'photo':
			# To do
			bot.sendPhoto(chat_id, msg['photo'][2]['file_id'], caption=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)
    
    def on__idle(self, event):
        self.close()
        
			
# One ButtonHandler created per message that has a button pressed.
# There should only be one message from the bot at a time in a chat, so that
# you modify the same message over and over again.
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
	def __init__(self, *args, **kwargs):
		super(ButtonHandler, self).__init__(*args, **kwargs)
		self.state = None
		self.chat_id = None

	def placesNearBy(self, establishmentType, chat_id):
		data = db.getLocation(chat_id)
		latitude = data[0]
		longitude = data[1]
		js = mapclient.places_nearby(location=(latitude, longitude), type=establishmentType, language='es-ES', radius=2000, min_price=0, max_price=4, open_now=True)
		if js["status"] != 'ZERO_RESULTS':
			self.editor.editMessageText('Choose one', reply_markup=keyboards.resultsKeyboard(js))
		else:
			self.editor.editMessageText("There aren't establishment available with this parameters", reply_markup=keyboards.inlineBack)
		    
	def on_callback_query(self, msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		bot.answerCallbackQuery(query_id)
		
		if self.state == None:
			self.state = steps.getStep(from_id)
			self.chat_id = from_id
		
		if query_data == "back":
			stp = steps.stepBack(self.state)	
			if stp != False:
				self.state -= 1;
				if stp == "Init":
					bot.sendMessage(from_id, 'Share your location', reply_markup=keyboards.markupLocation)
				elif stp == "Choose Type":
					self.editor.editMessageText('What are you looking for?', reply_markup=keyboards.inlineEstablishment)
				elif stp == "Choose Establish":
					eType = db.getEType(from_id)			
					self.placesNearBy(eType, from_id) 
				# Caso de estar mandando una foto			
					
		elif steps.step(self.state) == "Choose Type":
			self.state = steps.nextStep(self.state)
			db.storeEType(from_id, query_data)
			self.placesNearBy(query_data, from_id)			
			
		elif steps.step(self.state) == "Choose Establish":
			self.state = steps.nextStep(self.state)
			steps.saveStep(self.chat_id, self.state) # After this point, the flow of options of the user can branch
			data = query_data.split(" ")
			lat = data[0]
			lng = data[1]
			bot.sendLocation(from_id,lat,lng)	
			bot.sendMessage(from_id,"Here it is", reply_markup=keyboards.optionsKeyboard(query_data))
			
		elif steps.step(self.state) == "Info Establish":
			option = query_data.split(" ")
			
			if 	option[0] == "rating":
				# To do
				print('Do something with the rating.')
				
			elif option[0] == "photo":
				preparePhotoSending(from_id, msg['message_id'], [loc[1],loc[2]])
				self.editor.editMessageText('Send us a photo of the place!', reply_markup=keyboards.inlineBack)
			
	def on__idle(self, event):
		steps.saveStep(self.chat_id, self.state)
		self.close()

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=180),
    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=180),
])

bot.message_loop(run_forever='Listening')

