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
import datetime
import db
import steps

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
#KeyboardMarkups
markupLocation = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Location', request_location=True)],], resize_keyboard=True, one_time_keyboard=True)
#markupBack = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Back')],], resize_keyboard=True)

#InlineKeyboards
inlineEstablishment = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Bar', callback_data='bar')] + [InlineKeyboardButton(text='Cafe', callback_data='cafe')],
					[InlineKeyboardButton(text='Food', callback_data='food')]+ [InlineKeyboardButton(text='Night club', callback_data='night_club')],
					[InlineKeyboardButton(text='Restaurant', callback_data='restaurant')], [InlineKeyboardButton(text='Back', callback_data='back')],
               ])
inlineBack = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data='back')],])

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
				bot.sendMessage(chat_id, 'Share your location', reply_markup=markupLocation)
		elif content_type == 'location':
			db.storeLocation(chat_id, msg['location'])
			#thanks = 'Thanks ' + msg['chat']['first_name']
			#bot.sendMessage(chat_id, thanks, reply_markup=markupBack)
			steps.nextStep(chat_id)
			bot.sendMessage(chat_id, 'What are you looking for?', reply_markup=inlineEstablishment)			
    
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
			i = 0
			row = [] 
			keyboardRestaurant= []
			for j in js["results"]:
				loc = str(j["geometry"]["location"]["lat"]) + " " + str(j["geometry"]["location"]["lng"])
				if len(j["name"]) > 15:
					i = 0
					keyboardRestaurant.append(row)
					row = [InlineKeyboardButton(text=j["name"], callback_data=loc)]
					keyboardRestaurant.append(row)
					row = []
				elif i == 2:
					i = 0
					keyboardRestaurant.append(row)
					row = [InlineKeyboardButton(text=j["name"], callback_data=loc)]
				else:
					row = row + [InlineKeyboardButton(text=j["name"], callback_data=loc)]
				i += 1
			row = [InlineKeyboardButton(text='Back', callback_data='back')]
			keyboardRestaurant.append(row)
			markupRestaurant = InlineKeyboardMarkup(inline_keyboard = keyboardRestaurant)
			self.editor.editMessageText('Choose one', reply_markup=markupRestaurant)
		else:
			self.editor.editMessageText("There aren't establishment available with this parameters", reply_markup=markupRestaurant)
		    
    def on_callback_query(self, msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		bot.answerCallbackQuery(query_id)

		if query_data == "back":
			stp = steps.stepBack(from_id)	
			if stp != False:
				if stp == "Init":
					bot.sendMessage(from_id, 'Share your location', reply_markup=markupLocation)
				elif stp == "Choose Type":
					bot.sendMessage(from_id, 'What are you looking for?', reply_markup=inlineEstablishment)
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
			self.editor.editMessageText("Here it is", reply_markup=inlineBack)
			bot.sendLocation(from_id,lat,lng)			
            
    def on__idle(self, event):
        self.close()
			
TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=3),
    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=3),
])

bot.message_loop(run_forever='Listening')
