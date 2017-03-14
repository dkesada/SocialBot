#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes
import db
listSteps = ["Init","Choose Type", "Choose Establish", "Send Location", "Info Establish"]

# Mejor que estar llamando a la base todo el rato por el step, hacemos un atributo privado
# de la clase button handler que sea el step, y al crear un objeto de esa clase que lo busque en la base de datos
# y al ocurrir el on_idle lo guardamos. Así ahorramos bastantes llamadas con un timeout de un par de minutos

def step(chat_id):
	stp = db.getStep(chat_id)
	i = stp['step']
	return listSteps[i]
	
def nextStep(chat_id):
	stp = db.getStep(chat_id)
	i = stp['step']
	if i < len(listSteps)-1:
		db.setStep(chat_id, i+1)
		
def stepBack(chat_id):
	stp = db.getStep(chat_id)
	i = stp['step']
	if i != 0:
		i -= 1
		db.setStep(chat_id, i)
		return listSteps[i]
	else:
		return False
