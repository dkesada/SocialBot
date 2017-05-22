#! /usr/bin/python
#-*. coding: utf-8 -*-
# David Quesada López
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
El bot permite jugar partidas de 3 en raya contra un oponente aleatorio. 

La idea del bot no es tanto las partidas de 3 en raya, que es algo muy simple, 
sino el uso del delegator bot ofrecido por telepot, el uso de clases, la creación de 
un gestionador sencillo que irá por detrás funcionando como demonio, 
asignando parejas de oponentes según vayan llegando y el uso de la modificación de mensajes
para darle al inline keyboard una mayor vistosidad y utilidad.

He intentado llevar el uso de los inline keyboards a su máximo exponente usando la función
de modificar mensajes anteriores. De esta forma, la interfaz puede constar de un solo mensaje
que se va modificando según qué vayas haciendo (en este caso colocar fichas).
De este modo, no tienes que gestionar que el usuario pulse un botón inesperado (si le mandas
un inline keyboard y luego otro mensaje con un keyboard diferente, el usuario sigue podiendo
pulsar botones de mensajes anteriores, y eso conlleva errores inesperados).

El inline keyboard con modificación de mensajes ofrece una posibilidad para simular
una interfaz limpia y fija, aunque hay que estar atento de si se van a mandar mensajes después
que deberían persistir, acordarse de usar la función de eliminar mensaje para borrar los 
inline keyboards que hayan quedado atrás en la conversación.
"""

partidas = {}
q = Queue()

# El gestionador lleva todo lo relacionado con crear partidas y terminarlas
class Gestionador(threading.Thread):
    def __init__(self, cola):
        threading.Thread.__init__(self)
        self.cola = cola
        self.num = 0
        self.ids = [1,2]
    
    def run(self):
        while(True):
            mensaje = self.cola.get()
            if mensaje[0] is 'pair':
                self.peticion(mensaje[1])
            elif mensaje[0] is 'delPair':
                del partidas[mensaje[1]]
            time.sleep(3)
            
    def peticion(self, x):
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

# GameStarter inicializa
class GameStarter(telepot.helper.ChatHandler):
    def __init__(self, *args, **kwargs):
        super(GameStarter, self).__init__(*args, **kwargs)

    def on_chat_message(self, msg):
        content_type, chat_type, chat_id = telepot.glance(msg)
        self.sender.sendMessage(
            'Pulsa START para buscar una partida.',
            reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='START', callback_data='start'),
                ]]
            )
        )

        self.close()  # Dejas que Game se haga cargo de las partidas

class Game(telepot.helper.CallbackQueryOriginHandler):
    def __init__(self, *args, **kwargs):
        super(Game, self).__init__(*args, **kwargs)
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.tipo = ' '
        self.fid = 0

    def _next_move(self):
        msg = self.representateKeyboard() 
        self.editor.editMessageText(msg, reply_markup=None)
        mov = partidas[self.fid][2].get() # Si no te toca esperas el siguiente movimiento
        self.board[mov[0]] = mov[1]
        self.comprobarFin()
        msg = 'Tu turno.'
        keyboard = self.createKeyboard()
        
        self.editor.editMessageText(msg,reply_markup=keyboard)

    def on_callback_query(self, msg):
        mal = False
        query_id, from_id, query_data = telepot.glance(msg, flavor='callback_query')
        bot.answerCallbackQuery(query_id)
        if query_data == 'start':
            self.fid = from_id
            q.put(['pair', from_id])
            while from_id not in partidas:
                time.sleep(2)
            self.tipo = partidas[from_id][1]
        else:
            if self.board[int(query_data)] == ' ': # Me aseguro de que ha pulsado una posicion vacia
                self.movimiento(int(query_data))
                self.comprobarFin()
            else:
                print("mal")
                mal = True
        if not mal:
            self._next_move()

    def on__idle(self, event): # Si no se hace nada durante un tiempo se acaba la partida
        text = 'Partida terminada por inactividad.'
        self.editor.editMessageText(text, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='START', callback_data='start'),
                ]]))
        q.put(['delPair', self.fid])
        self.close()
        
    def movimiento(self,pos): # Manda un movimiento a tu oponente
        self.board[pos] = self.tipo
        partidas[partidas[self.fid][0]][2].put([pos,self.tipo])
    
    def createKeyboard(self): # Crea un teclado con el tablero que se le da
        botones = []
        for i in [0,3,6]:
            botones.append([InlineKeyboardButton(text=self.board[i], callback_data=str(i)),
                            InlineKeyboardButton(text=self.board[i+1], callback_data=str(i+1)),
                            InlineKeyboardButton(text=self.board[i+2], callback_data=str(i+2))])
        return InlineKeyboardMarkup(inline_keyboard = botones)
    
    def representateKeyboard(self): # Crea una representacion en texto del tablero
        rep = ''
        for i in [0,3,6]:
            rep = rep + '|'+ self.board[i] +'|' + self.board[i+1] + '|' + self.board[i+2] + '| \n'
            
        return rep
        
    def comprobarFin(self): # Mira si la partida la ha ganado alguno de los 2
        a = 'xxx'
        b = 'ooo'
        row = ''
        for i in [0,3,6]: # filas
            row = row.join(self.board[i:i+3])
            if a == row or b == row:
                self.finalizar(i)
            row = ''
        
        for i in range(3): # columnas
            row = row.join(self.board[i::3])
            if a == row or b == row:
                self.finalizar(i)
            row = ''
        
        # diagonales
        row = row.join(self.board[0::4])
        if a == row or b == row:
            self.finalizar(0)
        row = ''
        row = row.join([self.board[2],self.board[4],self.board[6]])
        if a == row or b == row:
            self.finalizar(2)
        row = ''
        # empate
        if row.join(self.board).find(' ') == -1:
            self.finalizar(-1)
            
    def finalizar(self, pos):
        msg = 'Empate'
        if pos > -1:
            if self.tipo == self.board[pos]:
                msg = 'Has ganado'
            else:
                msg = 'Has perdido'
        self.editor.editMessageText(msg, reply_markup=InlineKeyboardMarkup(
                inline_keyboard=[[
                    InlineKeyboardButton(text='START', callback_data='start'),
                ]]))
        q.put(['delPair', self.fid])
        self.close()
                    

# Lanzo a ejecutar el hilo del controlador nada más conectar el bot
gest = Gestionador(q)
gest.setDaemon = True
gest.start()

TOKEN = '255866015:AAFvI3sUR1sOFbeDrUceVyAs44KlfKgx-UE'

bot = telepot.DelegatorBot(TOKEN, [
    pave_event_space()(
        per_chat_id(), create_open, GameStarter, timeout=10),
    pave_event_space()(
        per_callback_query_origin(), create_open, Game, timeout=30),
])

bot.message_loop()
