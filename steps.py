#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes
import db
listSteps = ["Init","Choose Type", "Choose Establish", "Info Establish", "Rating", "Viewing Photos", "Come Back"]

# Mechanism that allows the "back" function by storing the state of the user

def step(state):
	return listSteps[state]
	
def nextStep(state):
	if state < len(listSteps)-1:
		if state == 4: #Rating
			state += 1
		return state + 1
	else:
		return state
		
def stepBack(state):
	if state != 0:
		if state == 5:
			return listSteps[3]
		state -= 1
		return listSteps[state]
	else:
		return False

def getStep(chat_id):
	return db.getStep(chat_id)['step']

def saveStep(chat_id, state):
	db.setStep(chat_id, state)

