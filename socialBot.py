#! /usr/bin/python
#-*. coding: utf-8 -*-

import sys
import time
import threading
from Queue import Queue
import telepot
import telepot.helper
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.delegate import (
    per_chat_id, per_callback_query_origin, create_open, pave_event_space)

"""
Deberíamos empezar de más simple a más complejo, del palo de primero la interfaz
con algún botón, que nos manden su ubicación y mostrar los locales cercanos.
Luego para la base de datos yo preferiría usar mongodb, parece más adecuado para este caso
que sql. De primeras a la base de datos irían los usuarios que entren y luego los locales de
los que tengamos algún dato. O dos colecciones de mongo o todo en la misma, por evitar los 
join si hubiese.
Vamos a intentar desde el principio poner todo el código en inglés, y eso que nos ahorramos
para luego.

Para mirar cosas del telepot la mejor documentacion es esta:

http://telepot.readthedocs.io/en/latest/reference.html

Ahí se puede buscar las funciones en concreto, lo que devuelven, lo que necesitan,...
No está muy allá en algunos casos pero bueno, menos es nada. Entre eso y los ejemplos del tio
va bien.


"""


# One UserHandler created per chat_id. May be useful for sorting out users
# Handles chat messages, we should sort out with telepot.glance what to do with the
# message depending on its type (text, image, location,...)
class UserHandler(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(UserHandler, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg,flavor='chat')
        # Some content_type values: text, location, photo
        
        if content_type == 'text':
            
        elif content_type == 'location':
        

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

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, UserHandler, timeout=10),
    pave_event_space()(
        per_callback_query_origin(), create_open, ButtonHandler, timeout=30),
])

bot.message_loop()
