import pymongo
from pymongo import MongoClient

connection = MongoClient('localhost', 27017)
db = connection.bot
users = db.users
    
def storeLocation(chat_id, loc):
    users.update_one({'_id':chat_id},{'$set':{'location':loc}},upsert=True)
    
def getLocation(chat_id):
    loc = users.find_one({'_id':chat_id},{'_id':0, 'location': 1})
    return [loc['location']['latitude'],loc['location']['longitude']]

def	setStep(chat_id, step):
    users.update_one({'_id':chat_id},{'$set':{'step': step}},upsert=True)
    
def getStep(chat_id):
    return users.find_one({'_id':chat_id},{'_id':0, 'step': 1})
