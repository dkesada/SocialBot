#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton
import db

#KeyboardMarkups
markupLocation = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Location', request_location=True)],], resize_keyboard=True, one_time_keyboard=True)

#InlineKeyboards
inlineEstablishment = InlineKeyboardMarkup(inline_keyboard=[
                   	[InlineKeyboardButton(text='Bar', callback_data='bar')] + [InlineKeyboardButton(text='Cafe', callback_data='cafe')],
					[InlineKeyboardButton(text='Food', callback_data='food')]+ [InlineKeyboardButton(text='Night club', callback_data='night_club')],
					[InlineKeyboardButton(text='Restaurant', callback_data='restaurant')], [InlineKeyboardButton(text='Back', callback_data='back')],
               ])
inlineBack = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Back', callback_data='back')],])

rating = InlineKeyboardMarkup(inline_keyboard=[
		[InlineKeyboardButton(text='0', callback_data='0')] + [InlineKeyboardButton(text='1', callback_data='1')] + [InlineKeyboardButton(text='2', callback_data='2')],
		[InlineKeyboardButton(text='3', callback_data='3')] + [InlineKeyboardButton(text='4', callback_data='4')] + [InlineKeyboardButton(text='5', callback_data='5')], [InlineKeyboardButton(text='Back', callback_data='back')]])
		
afterRate = InlineKeyboardMarkup(inline_keyboard=[
					[InlineKeyboardButton(text='Choose location', callback_data='init')],
					[InlineKeyboardButton(text="Choose establishment's type", callback_data='type')],
					[InlineKeyboardButton(text='Choose establishment', callback_data='establishment')],	
               ])#Volver a puntuacion, fotos etc

def resultsKeyboard(js):
	"""Keyboard that displays the results of a location query."""
	i = 0
	row = [] 
	keyboardRestaurant= []
	for j in js["results"]:
		loc = str(j["geometry"]["location"]["lat"]) + " " + str(j["geometry"]["location"]["lng"])
		if len(j["name"]) > 15:			
			i = -1
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
	keyboardRestaurant.append(row)
	row = [InlineKeyboardButton(text='Back', callback_data='back')]
	keyboardRestaurant.append(row)
	markupRestaurant = InlineKeyboardMarkup(inline_keyboard = keyboardRestaurant)
	
	return markupRestaurant

def optionsKeyboard(loc):
	"""Keyboard that shows the posible options for a displayed place."""
	kboard = []
	info = db.getPlaceData(loc)
	loc = str(loc[0]) + " " + str(loc[1])
	res = [InlineKeyboardButton(text="Rate it", callback_data="rating " + loc)] + [InlineKeyboardButton(text="Send a photo", callback_data="photo " + loc)]
	kboard.append(res)
	if info != None:
		if 'photos' in info:
			res = [InlineKeyboardButton(text='Show photos', callback_data="show_photos " + loc)]	
			kboard.append(res)
	res = [InlineKeyboardButton(text='Back', callback_data='back')]
	kboard.append(res)
	markupOptions = InlineKeyboardMarkup(inline_keyboard = kboard)
	return markupOptions
	
def photos(info, pos):
	kboard = []
	res = []
	if pos > 0:
		res = [InlineKeyboardButton(text="Previous photo", callback_data=str(pos-1))]
	if pos+1 < len(info['photos']):
		res += [InlineKeyboardButton(text="Next photo", callback_data=str(pos+1))]
	kboard.append(res)
	res = [InlineKeyboardButton(text='Back', callback_data='back')]
	kboard.append(res)
	markupPhotos = InlineKeyboardMarkup(inline_keyboard = kboard)
	return markupPhotos
	
