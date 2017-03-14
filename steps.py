
import db
listSteps = ["Init","Choose Type", "Choose Establish", "Send Location"]
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
