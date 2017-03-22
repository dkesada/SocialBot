#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes
import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.bot
users = db.users
places = db.places
    
def storeLocation(chat_id, loc, date):
    users.update_one({'_id':chat_id},{'$set':{'location':loc, 'date':date}},upsert=True)
    
def getLocation(chat_id):
    loc = users.find_one({'_id':chat_id},{'_id':0, 'location': 1})
    return [loc['location']['latitude'],loc['location']['longitude']]

def setStep(chat_id, step):
    users.update_one({'_id':chat_id},{'$set':{'step': step}},upsert=True)
    
def getStep(chat_id):
    return users.find_one({'_id':chat_id},{'_id':0, 'step': 1})
		
def storeEType(chat_id, eType):
	users.update_one({'_id':chat_id}, {'$set':{'eType':eType}},upsert=True)

def getEType(chat_id):
	eType = users.find_one({'_id':chat_id},{'_id':0, 'eType': 1})
	return eType['eType']

def getPlaceData(loc):
	return places.find_one({'loc':loc},{'_id':0})
	
def storeRating(loc,chat_id, rating):
	previousRating = places.find_one({'loc':loc,'ratings.user':chat_id})
	if previousRating == None:
		places.update_one({'loc':loc}, {'$inc':{"ratings.$.rate":rating}}, upsert=True)
		places.update_one({'loc':loc,'ratings.user':chat_id}, {'$set':{"ratings.$.rate":rating}})
	
	
def storePlacePhoto(loc, photo):
	places.update({'loc':loc},{'$push':{'photos':photo}})
