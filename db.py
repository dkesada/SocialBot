#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes
import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.bot
users = db.users
places = db.places
    
def storeLocation(chat_id, loc, date):
	"""Stores the current location of the user."""
	users.update_one({'_id':chat_id},{'$set':{'location':loc, 'date':date}},upsert=True)
    
def getLocation(chat_id):
	"""Returns the current location of the user."""
	loc = users.find_one({'_id':chat_id},{'_id':0, 'location': 1})
	return [loc['location']['latitude'],loc['location']['longitude']]

def setStep(chat_id, step):
	"""Stores the current step of the user."""
	users.update_one({'_id':chat_id},{'$set':{'step': step}},upsert=True)
    
def getStep(chat_id):
	"""Returns the current step of the user."""
	return users.find_one({'_id':chat_id},{'_id':0, 'step': 1})
		
def storeEType(chat_id, eType):
	"""Stores the type of stablishment that the user selected."""
	users.update_one({'_id':chat_id}, {'$set':{'eType':eType}},upsert=True)

def getEType(chat_id):
	"""Returns the type of stablishment that the user selected."""
	eType = users.find_one({'_id':chat_id},{'_id':0, 'eType': 1})
	return eType['eType']

def getPlaceData(loc):
	"""Returns all the data stored of a place."""
	return places.find_one({'loc':loc},{'_id':0})
	
def storeRating(loc, chat_id, rate):
	"""Stores an user rating of a stablishment."""
	previousRate = places.find_one({'loc':loc, 'user':chat_id}, {'_id':0, 'rate':1})
	places.update_one({'loc':loc, 'user':chat_id}, {'$set': {'rate':rate}},upsert=True)
	incr = 1
	if previousRate != None:
		pRate = previousRate['rate']
		rate = rate - pRate
		incr = 0
	previousRating = places.find_one({'loc':loc}, {'_id':0, 'ratings':1})
	if previousRating != None:
		places.update_one({'loc':loc}, {'$inc': {'ratings.rate':rate, 'ratings.numRate':incr}})	
	else:
		places.update_one({'loc':loc}, {'$set': {'ratings.rate':rate, 'ratings.numRate':1}},upsert=True)
	
def storePlacePhoto(loc, photo):
	"""Stores a file_id from a photo of a stablishment sent by an user."""
	places.update({'loc':loc},{'$push':{'photos':photo, "$slice":-5}}) # Slice limits the photo array
	
def preparePhotoSending(chat_id, message_id, loc):
	"""Prepares de user for a photo sending. This stores the message_id to modify the markup, the location that is receiving a photo and a flag."""
	users.update_one({'_id':chat_id},{'$set':{'sending':{'type':'photo', 'msg_id':message_id, 'location':loc}}},upsert=True)

def getPlacePhotos(loc):
	"""Returns all the photos of a given place."""
	return places.find_one({'_id':loc},{'_id':0, 'photos':1})

def getSending(chat_id):
	"""Returns the info of the next sending that the user will perform."""
	return users.find_one({'_id':chat_id},{'_id':0,'sending':1})
	
def endSending(chat_id):
	"""Finishes a sending for the chat_id"""
	users.update_one({'_id':chat_id},{'$unset':{'sending':""}})

