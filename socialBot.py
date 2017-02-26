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

"""
He empezado a usar esto para sacar los locales cercanos a la ubicación que te manden:
https://github.com/googlemaps/google-maps-services-python

Con 'pip install -U googlemaps' basta para poder usarlo
La clave de la api de google la introduzco por consola, para no tenerla publicada en github

Aquí está la documentación de las funciones que tiene:
https://googlemaps.github.io/google-maps-services-python/docs/2.4.5/

Por ahora he estado probando el de places_nearby, que funciona devolviendo un json con los 
resultados de la búsqueda que hayas puesto. Los parámetros de la función vienen explicados
en la documentación


Documentacion de telepot:
http://telepot.readthedocs.io/en/latest/reference.html

"""

# Readying the google maps client

mapclient = googlemaps.Client(key=sys.argv[1]) # Input the api key as the first argument when launching

#clients = {}
#q = Queue()
# The manager takes everything about creating conexions and to finish them
class Manager(threading.Thread):
    def __init__(self, queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.num = 0
        self.ids = [1,2]
    
    def run(self):
        while(True):
            message = self.queue.get()
            if message[0] is 'pair':
                self.request(message[1])
            elif message[0] is 'delPair':
                del clients[message[1]]
            time.sleep(3)
            
    def request(self, x):
        if self.num == 1 and self.ids[0] != x:
            self.ids[1] = x
            q1 = Queue()
            q1.put([0,' '])
            q2 = Queue()
            partidas[self.ids[0]] = [self.ids[1],'x',q1]
            partidas[self.ids[1]] = [self.ids[0],'o',q2]
            self.num = 0
        else:
            self.ids[0] = x
            self.num = 1

# One UserHandler created per chat_id. May be useful for sorting out users
# Handles chat messages, we should sort out with telepot.glance what to do with the
# message depending on its type (text, image, location,...)
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg,flavor='chat')
        if content_type == 'text':	
            markup = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Location', request_location=True)],])
            bot.sendMessage(chat_id, 'Share your location', reply_markup=markup)
					
        elif content_type == 'location':
            print(msg['location']['latitude'])
            print(mapclient.places_nearby(location=(msg['location']['latitude'], msg['location']['longitude']),
                           type='restaurant', language='es-ES', radius=2000,
                           min_price=1, max_price=4, open_now=True))

            

# One ButtonHandler created per message that has a button pressed.
# There should only be one message from the bot at a time in a chat, so that
# you modify the same message over and over again.
class ButtonHandler(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(ButtonHandler, self).__init__(*args, **kwargs)
        
    def on_callback_query(self, msg):
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        bot.answerCallbackQuery(query_id)

            
# El token si quieres puedo ponerlo para que lo pongamos por consola como argumento al 
# lanzar el bot
TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'
#manage = Manager(q)
#manage.setDaemon = True
#manage.start()

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=10),
    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=30),
])

bot.message_loop(run_forever='Listening')
