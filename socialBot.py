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
import math
import json
import datetime
import db
import steps
import keyboards
import translate

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap

"""
Api para sacar los locales cercanos a la ubicación que te manden:
https://github.com/googlemaps/google-maps-services-python

Aquí está la documentación de las funciones que tiene:
https://googlemaps.github.io/google-maps-services-python/docs/2.4.5/

Documentacion de telepot:
http://telepot.readthedocs.io/en/latest/reference.html
https://core.telegram.org/bots


http://qingkaikong.blogspot.com.es/2016/02/plot-earthquake-heatmap-on-basemap-and.html
"""

# Readying the google maps client

mapclient = googlemaps.Client(key=sys.argv[1]) #Input the api places key as the first argument when launching
geoClient = googlemaps.Client(key=sys.argv[2]) #Input the api geocode key as the first argument when launching

# One UserHandler created per chat_id. May be useful for sorting out users
# Handles chat messages depending on its tipe
class UserHandler(telepot.helper.ChatHandler):
	def __init__(self, *args, **kwargs):
		super(UserHandler, self).__init__(*args, **kwargs)

	def calculateBounds(self, kmeters, loc):
		R=6367.45 #media geometrica
		bearing = math.radians(45) #45º
		lat = math.radians(loc[0]) #lat of the user
		lon = math.radians(loc[1]) #lng of the user
		latup = math.asin(math.sin(lat)*math.cos(kmeters/R) + math.cos(lat)*math.sin(kmeters/R)*math.cos(bearing))
		lonup = lon + math.atan2(math.sin(bearing)*math.sin(kmeters/R)*math.cos(lat), math.cos(kmeters/R)-math.sin(lat)*math.sin(latup))
		dlat=latup-lat
		dlng=lonup-lon
		latdw = lat-dlat
		londw = lon-dlng
		latup = math.degrees(latup)
		lonup = math.degrees(lonup)
		latdw = math.degrees(latdw)
		londw = math.degrees(londw)
		
		return londw, latdw, lonup, latup   
		
	def heatmap(self, allLoc, chat_id):
		ln = []
		lt = []
		for geo in allLoc:
			if geo != {}:
				ln.append(geo['location']['longitude'])
				lt.append(geo['location']['latitude'])
		loc = db.getLocation(chat_id)
		llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat= self.calculateBounds(2., loc)
		#3857 o 4326
		map = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat, epsg=4326)
		map.arcgisimage(service='World_Imagery', xpixels = 1500, verbose= True)
		x,y = map(ln, lt)		
		map.plot(x, y, 'ro', markersize=5,markeredgecolor="none", alpha=0.33)
		x0, y0 = map(loc[1], loc[0])
		x1, y1 = map(loc[1]-0.001, loc[0]+0.0017)	
		plt.imshow(plt.imread('loc.png'),  extent = (x0, x1, y0, y1))
		plt.savefig("out.png")
		
	def on_chat_message(self, msg):
		content_type, chat_type, chat_id = telepot.glance(msg,flavor='chat')
		if content_type == 'text':
			if msg['text'] == "/start":
				steps.saveStep(chat_id, 1)
				lang = db.getLanguage(chat_id)
				bot.sendMessage(chat_id, translate.location(lang), reply_markup=keyboards.markupLocation(lang))
			elif msg['text'] == "/settings":
				steps.saveStep(chat_id, 0)	
				lang = db.getLanguage(chat_id)			
				bot.sendMessage(chat_id, translate.settings(lang), reply_markup=keyboards.settings(lang))
			elif msg['text'] == "/heatmap":
				locs = db.getAllLocations()
				self.heatmap(locs, chat_id)
				lang = db.getLanguage(chat_id)
				bot.sendMessage(chat_id, translate.takesFew(lang), reply_markup=None)
				bot.sendPhoto(chat_id, open('out.png', 'rb'))
				bot.sendMessage(chat_id, translate.location(lang), reply_markup=keyboards.markupLocation(lang))
			elif msg['text'] == "Default" or msg['text'] == "Por defecto":
				db.storeLocation(chat_id, {u'latitude': 40.411085, u'longitude': -3.685014}, msg['date'])
				state = 1
				steps.saveStep(chat_id, steps.nextStep(state))
				lang = db.getLanguage(chat_id)
				bot.sendMessage(chat_id, translate.lookingFor(lang), reply_markup=keyboards.inlineEstablishment(lang))
			elif msg['text'] == "/help":
				steps.saveStep(chat_id, 8)	
				lang = db.getLanguage(chat_id)			
				bot.sendMessage(chat_id, translate.help(lang), reply_markup=keyboards.inlineBack(lang))
			elif msg['text'] == "/stats":
				steps.saveStep(chat_id, 9)	
				lang = db.getLanguage(chat_id)
				user = db.getRole(chat_id)
				if user == "superuser":
					stats = db.getStats()
					bot.sendMessage(chat_id, translate.stats(lang, stats), reply_markup=keyboards.inlineBack(lang))
				else:					
					bot.sendMessage(chat_id, translate.noSuperuser(lang), reply_markup=keyboards.inlineBack(lang))
			elif steps.getStep(chat_id) == 1:
				js = geoClient.geocode(address=msg['text'], components=None, bounds=None, region=None, language='es-ES')
				lang = db.getLanguage(chat_id)
				location = {u'latitude':js[0]['geometry']['location']['lat'], u'longitude':js[0]['geometry']['location']['lng']}
				bot.sendMessage(chat_id, translate.yourPosition(lang, js[0]['formatted_address']), reply_markup=None)
				db.storeLocation(chat_id, location, msg['date'])
				state = 1
				steps.saveStep(chat_id, steps.nextStep(state))				
				bot.sendMessage(chat_id, translate.lookingFor(lang), reply_markup=keyboards.inlineEstablishment(lang))
			else:
				lang = db.getLanguage(chat_id)
				bot.sendMessage(chat_id, translate.textNoProcces(lang), reply_markup=keyboards.markupLocation(lang))

		elif content_type == 'location':
			db.storeLocation(chat_id, msg['location'], msg['date'])
			state = 1
			steps.saveStep(chat_id, steps.nextStep(state))
			lang = db.getLanguage(chat_id)
			bot.sendMessage(chat_id, translate.lookingFor(lang), reply_markup=keyboards.inlineEstablishment(lang))
		elif content_type == 'photo':
			sending = db.getSending(chat_id)['sending']
			if sending != None and sending['type'] == 'photo':
				index = len(msg['photo'])-1
				db.storePlacePhoto(sending['location'], msg['photo'][index]['file_id'])
				lang = db.getLanguage(chat_id)
				bot.editMessageReplyMarkup(msg_identifier=(chat_id,sending['msg_id']), reply_markup=None)
				bot.sendMessage(chat_id, translate.photoRec(db.getLanguage(chat_id)), reply_markup=keyboards.optionsKeyboard(sending['location'], lang))
						
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
		self.loc = None
		self.language = None

	def placesNearBy(self, establishmentType, chat_id):
		data = db.getLocation(chat_id)
		latitude = data[0]
		longitude = data[1]
		settings = db.getSettings(chat_id)
		js = mapclient.places(None, location=(latitude, longitude), radius=settings['radius'], language='es-ES', min_price=None, max_price=None, open_now=settings['openE'], type=establishmentType)
		uLoc = db.getLocation(chat_id)
		message = translate.chooseOne(self.language)
		distanceL = {}
		rateL = {}
		if js["status"] != 'ZERO_RESULTS':
			for j in js["results"]:
				location = str(j["geometry"]["location"]["lat"]) + " " + str(j["geometry"]["location"]["lng"])
				#distance = "{0:.2f}".format(self.haversine(location, uLoc))
				distance = int((self.haversine(location, uLoc)))
				distanceL[distance] = j['name']
				rate = db.avgRatePlace([str(j["geometry"]["location"]["lng"]), str(j["geometry"]["location"]["lat"])])
				if rate != None:
					rateL[rate] = j['name']
			rates = sorted(rateL, reverse=True)
			pos = sorted(distanceL, key=int)
			message	+= translate.prox(self.language, distanceL, pos)
			if rateL != {}:
				message	+= "\n"
				message	+= translate.rated(self.language, rateL, rates)
			self.editor.editMessageText(message, reply_markup=keyboards.resultsKeyboard(js, self.language))			
		else:
			self.editor.editMessageText(translate.noEstablish(self.language), reply_markup=keyboards.inlineBack(self.language))
		    
	def on_callback_query(self, msg):
		query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
		#bot.answerCallbackQuery(query_id)

		if self.state == None:
			self.state = steps.getStep(from_id)
			self.chat_id = from_id
			sending = db.getSending(self.chat_id)
			self.language = db.getLanguage(self.chat_id)
			if sending != None and 'sending' in sending:
				self.loc = sending['sending']['location']
				
		if query_data == "back":
			stp = steps.stepBack(self.state)	
			if stp != False:
				self.state -= 1;
				if stp == "Init":
					self.state = 1;
					self.editor.editMessageText(translate.location(self.language), reply_markup=None)
				elif stp == "Choose Type":
					self.editor.editMessageText(translate.lookingFor(self.language), reply_markup=keyboards.inlineEstablishment(self.language))
				elif stp == "Choose Establish":
					eType = db.getEType(from_id)			
					self.placesNearBy(eType, from_id)
				elif stp == "Info Establish":
					self.state -= 1;
					steps.saveStep(from_id, self.state)
					self.editor.editMessageReplyMarkup(reply_markup=None)
					bot.sendMessage(self.chat_id, translate.whatWant(self.language), reply_markup=keyboards.optionsKeyboard(self.loc, self.language))
							
		elif steps.step(self.state) == "Settings":
			if query_data == "language":
				self.editor.editMessageText(translate.chooseLang(self.language), reply_markup=keyboards.languages(self.language))
			elif query_data == "parameters":
				self.editor.editMessageText(translate.choooseParam(self.language), reply_markup=keyboards.parameters(self.language))
			elif query_data == "sback":				
				self.editor.editMessageText(translate.settings(self.language), reply_markup=keyboards.settings(self.language))
			elif query_data == "radius":
				self.editor.editMessageText(translate.choooseDistance(self.language), reply_markup=keyboards.radius(self.language))
			elif query_data == "open":
				self.editor.editMessageText(translate.onlyOpen(self.language), reply_markup=keyboards.openE(self.language))
			elif query_data == "numResults":
				self.editor.editMessageText(translate.howLocals(self.language), reply_markup=keyboards.numE(self.language))
			
			elif query_data == "restart":
				self.state = 1;
				steps.saveStep(self.chat_id, self.state)
				self.editor.editMessageText(translate.location(self.language), reply_markup=None)
			else:
				option = query_data.split(" ")
				if option[0] == "meters":
					meters = option[1]
					db.storeRadius(from_id, meters)
					bot.answerCallbackQuery(query_id, translate.radiusChanged(self.language))
					self.editor.editMessageText(translate.whatWant(self.language), reply_markup=keyboards.optionChanged(self.language))
				elif option[0] == "bool":
					openE = option[1]
					db.storeOpen(from_id, openE)
					bot.answerCallbackQuery(query_id, translate.openChanged(self.language))
					self.editor.editMessageText(translate.whatWant(self.language), reply_markup=keyboards.optionChanged(self.language))
				elif option[0] == "language":
					self.language = option[1]
					db.storeLanguage(from_id, self.language)
					bot.answerCallbackQuery(query_id, translate.languageChanged(self.language))
					self.editor.editMessageText(translate.whatWant(self.language), reply_markup=keyboards.optionChanged(self.language))
				elif option[0] == "num":
					num = option[1]
					db.storeNumberE(from_id, num)
					bot.answerCallbackQuery(query_id, translate.whatWant(self.language))
					self.editor.editMessageText(translate.whatWant(self.language), reply_markup=keyboards.optionChanged(self.language))
						
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
			self.loc = [lng, lat]
			bot.sendLocation(from_id,lat,lng)
			self.editor.editMessageReplyMarkup(reply_markup=None)	
			bot.sendMessage(from_id, translate.hereIts(self.language), reply_markup=keyboards.optionsKeyboard(self.loc, self.language))
			
		elif steps.step(self.state) == "Info Establish":
			option = query_data.split(" ")
			if option[2] is None:
				print option
			self.loc = [option[1], option[2]]
			if 	option[0] == "rating":
				self.state = steps.nextStep(self.state)
				self.editor.editMessageText(translate.yourRate(self.language), reply_markup=keyboards.rating(self.language))
								
			elif option[0] == "photo":
				db.preparePhotoSending(from_id, msg['message']['message_id'], self.loc)
				self.editor.editMessageText(translate.sendPhoto(self.language), reply_markup=keyboards.inlineBack(self.language))
				
			elif option[0] == "show_photos":
				self.state = steps.nextStep(self.state) + 1
				steps.saveStep(self.chat_id, self.state)
				info = db.getPlaceData(self.loc)
				db.preparePhotoSending(from_id, msg['message']['message_id'], self.loc)
				self.editor.editMessageReplyMarkup(reply_markup=None)
				bot.sendPhoto(from_id, info['photos'][0], reply_markup=keyboards.photos(info, 0, self.language))
				
		elif steps.step(self.state) == "Rating":
			db.storeRating(self.loc, from_id, int(query_data))
			self.state = steps.nextStep(self.state)
			star = u'\u2b50\ufe0f'
			text = ''
			for i in range(int(query_data)):
				text += star
			bot.answerCallbackQuery(query_id, text)
			self.editor.editMessageText(translate.whatWant(self.language), reply_markup=keyboards.optionsKeyboard(self.loc, self.language))
				
		elif steps.step(self.state) == "Viewing Photos":
			self.editor.editMessageReplyMarkup(reply_markup=None)
			info = db.getPlaceData(self.loc)
			bot.sendPhoto(from_id, info['photos'][int(query_data)], reply_markup=keyboards.photos(info, int(query_data), self.language))
			
			#self.state = steps.nextStep(self.state)
				
		elif steps.step(self.state) == "Come Back":
			if query_data == "init":
				self.state = 1
				self.editor.editMessageText(translate.location(self.language), reply_markup=None)
			elif query_data == "type":
				self.state = 2
				self.editor.editMessageText(translate.lookingFor(self.language), reply_markup=keyboards.inlineEstablishment(self.language))
			elif query_data == "establishment":
				self.state = 3
				eType = db.getEType(from_id)			
				self.placesNearBy(eType, from_id)
	
	def haversine(self, locat, uLoc):
		locat = locat.split(" ")
		lat2 = float(locat[0])
		lng2 = float(locat[1])
		lat1 = float(uLoc[0])
		lng1 = float(uLoc[1])
		rad=math.pi/180
		dlat=lat2-lat1
		dlng=lng2-lng1
		R=6367.45 #media geometrica
		a=(math.sin(rad*dlat/2))**2 + math.cos(rad*lat1)*math.cos(rad*lat2)*(math.sin(rad*dlng/2))**2
		distance=2*R*math.asin(math.sqrt(a))#kilometers
		return distance*1000#meters
				
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

