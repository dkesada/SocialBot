#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes

def location(lang):
	if lang == "Espanol":
		text = "¡Comparte tu localización! \n"
		text += "Si lo prefieres puedes escribir la dirección en la que te encuentras. O también la ciudad o el barrio "
		text += "en el que estás buscando los locales. \nTambién puedes probar el bot con la localización por defecto."
	else:
		text = "Share your location!\n"
		text += "If you prefer you can write the address you are in. Or also the city or neighborhood "
		text += "in which you are looking for the locals. \nYou can also test the bot with the default location."

	return text

def settings(lang):
	if lang == "Espanol":
		text = "Desde aquí puedes cambiar los ajustes de tu bot. En Escoge idioma tu puedes cambiar el idioma del bot. "
		text += "En Escoge parámetros puedes cambiar el radio de los establecimientos que quieres ir, si quieres "
		text += "el bot solo mostrará los locales que estén abiertos en el momento de la consulta."
	else:
		text = "From here you can change the settings of your bot. In Choose language you can change the language of the bot. "
		text += "In Choose parameters you can change the radius of the establishments you want to go, if you want "
		text += "the bot will only show the premises that are open at the time of the query."
		
	return text

def lookingFor(lang):
	if lang == "Espanol":
		return "¿Qué estás buscando?"
	else:
		return "What are you looking for?"

def photoRec(lang):
	if lang == "Espanol":
		return "¡Foto recibida, gracias! ¿Qué más quieres hacer?"
	else:
		return "Photo received, thank you! What more do you want to do?"

def chooseOne(lang):
	if lang == "Espanol":
		return "¡Escoge uno!\n"
	else:
		return "Choose one!\n"

def isv(lang):
	if lang == "Espanol":
		return " es "
	else:
		return " is "

def meters(lang):
	if lang == "Espanol":
		return " metros "
	else:
		return " meters "

def rate(lang):
	if lang == "Espanol":
		return "Y la puntuación de los usuarios es "
	else:
		return "And the rate of the users is "

def noEstablish(lang):
	if lang == "Espanol":
		return "No hay establecimientos con esos parámetros"
	else:
		return "There aren't any establishments with these parameters."

def whatWant(lang):
	if lang == "Espanol":
		return "¿Qué quieres hacer?"
	else:
		return "What do you want to do?"

def chooseLang(lang):
	if lang == "Espanol":
		return "Escoge tu idioma"
	else:
		return "Choose your language"

def choooseParam(lang):
	if lang == "Espanol":
		return "Escoge los parámetros de tu consulta (radio, abierto ahora, etc.):"
	else:
		return "Choose the parameters of your query (radio, open now, etc.):"

def choooseDistance(lang):
	if lang == "Espanol":
		return "Escoge una de las distancias que quieres establecer como radio de los locales que estás buscando. Las distancias están en metros."
	else:
		return "Choose one of the distances that you want to establish as a radio of the premises you are looking for. Distances are in meters."

def onlyOpen(lang):
	if lang == "Espanol":
		return "¿Sólo quieres ver establecimientos abiertos en el momento de la consulta?"
	else:
		return "Do you want to see only open establishments at the time of the query?"

def howLocals(lang):
	if lang == "Espanol":
		return "¿Cuántos establecimientos quieres ver?"
	else:
		return "How many establishments do you want to see?"

def radiusChanged(lang):
	if lang == "Espanol":
		return "Radio cambiado"
	else:
		return "Radius changed"

def openChanged(lang):
	if lang == "Espanol":
		return "Opción sólo abierto cambiada"
	else:
		return "Only open option changed"

def langChanged(lang):
	if lang == "Espanol":
		return "Idioma cambiado"
	else:
		return "Language changed"
		
def numberChanged(lang):
	if lang == "Espanol":
		return "Número de locales cambiado"
	else:
		return "Number of locals changed"

def hereIts(lang, rate, distance):
	star = u'\u2b50\ufe0f'
	if lang == "Espanol":
		text = "¡Aquí lo tienes!\nEstá a " + str(int(distance)) + " metros de ti "
		if rate != None:
			text += "y los usuarios lo han valorado con " + str(rate) + " " + star
	else:
		text = "Here it is!\nIt's " + str(int(distance)) + " meters away "
		if rate != None:
			text += "and users have rated it with " + str(rate) + " " + star
		
	return text

def yourRate(lang):
	if lang == "Espanol":
		return "Entonces ... ¿Cúal es tu puntuación?"
	else:
		return "So... What's your rate?"

def sendPhoto(lang):
	if lang == "Espanol":
		return "¡Envíanos una foto del lugar!"
	else:
		return "Send us a photo of the place!"

def markupLocation(lang):
	if lang == "Espanol":
		return ("Localización", "Por defecto")
	else:
		return ("Location", "Default")

def back(lang):
	if lang == "Espanol":
		return "Atrás"
	else:
		return "Back"
		
def settingsBoard(lang):
	text = []
	if lang == "Espanol":
		text = ["Escoge idioma", "Escoge parámetros", "Atrás"]
	else:
		text = ["Choose language", "Choose parameters", "Back"]
	return text
	
def inlineEstablishment(lang):
	text = []
	if lang == "Espanol":
		text = ["Bar", "Café", "Alimentación", "Local nocturno" "Restaurante", "Atrás"]
	else:
		text = ["Bar", "Cafe", "Food", "Night club", "Restaurant", "Back"]
	return text
	
def optionsKeyboard(lang):
	text = []
	if lang == "Espanol":
		text = ["Puntúalo", "Enviar una foto", "Mostrar fotos", "Atrás"]
	else:
		text = ["Rate it", "Send a photo", "Show photos", "Back"]
	return text
	
def parameters(lang):
	text = []
	if lang == "Espanol":
		text = ["Escoge el radio", "Escoge un número de locales", "Mostrar solo locales abiertos", "Atrás"]
	else:
		text = ["Choose the radius", "Choose a number of establishments", "Show only open establishments", "Back"]
	return text

def openE(lang):
	text = []
	if lang == "Espanol":
		text = ["Sí", "No", "Atrás"]
	else:
		text = ["Yes", "No", "Back"]
	return text
	
def optionChanged(lang): 
	text = []
	if lang == "Espanol":
		text = ["Menú de ajustes", "(Re)inicia el bot"]
	else:
		text = ["Settings", "(Re)Start the bot"]
	return text
	
def photos(lang):
	text = []
	if lang == "Espanol":
		text = ["Foto anterior", "Siguiente foto", "Atrás"]
	else:
		text = ["Previous photo", "Next photo", "Back"]
	return text

def takesFew(lang):
	if lang == "Espanol":
		return "La imagen tarda unos segundos en enviarse."
	else:
		return "The image takes a few seconds to send."

def help(lang):
	if lang == "Espanol":
		text = "La funcionalidad básica de @YourPlacesBot es ofrecerte todos los locales que tienes a tu alrededor. "
		text += "Para verlos solo debes envíar tu localización. Y podrás ver las puntuaciones y fotos de otros usuarios. "
		text += "Con el comando /settings puedes cambiar la configuración del bot, como el idioma, el radio de las consultas y más. "
		text += "Con /heatmap el bot te ofrece un mapa de calor de las zonas cercanas a tu posición."
	else:
		text = "The basic functionality of @YourPlacesBot is to offer you all the premises that you have around you. "
		text += "To see them you just have to send your location. And you can see the rates and photos of other users.  "
		text += "With the command /settings you can change the configuration of the bot, such as the language, the radius of queries and more. "
		text += "With /heatmap the bot gives you a heat map of the areas near your position. "
		
	return text
	
def textNoProcces(lang):
	if lang == "Espanol":
		return "Si quieres escribir una dirección primero introduce el comando /start, envíalo y luego escribe la dirección. "
	else:
		return "If you want to write an address first enter the command /start, send it and then write the address."

def yourPosition(lang, pos):
	if lang == "Espanol":
		return "Tu posición es  " + pos.encode('utf-8')
	else:
		return "Your position is " + pos.encode('utf-8')
		
def prox(lang, prlist, pos):
	first = prlist[pos[0]] + " (" + str(pos[0]) + " m)"
	if lang == "Espanol":
		text =  "Los más cercanos son " + first.encode('utf-8')
	else:
		text = "The closest ones are " + first
	
	if len(prlist) > 1:
		second = ", " + prlist[pos[1]] + " (" + str(pos[1]) + " m)"
		if lang == "Espanol":
			text += second.encode('utf-8')
		else:
			text +=  second	
	if len(prlist) > 2:
		third = prlist[pos[2]] + " (" + str(pos[2])+ " m)"
		if lang == "Espanol":
			text += " y " + third.encode('utf-8') + ".\n"
		else:
			text += " and " + third + ".\n"	
			
	return text
		
def rated(lang, prlist, pos):
	star = u'\u2b50\ufe0f'
	first = prlist[pos[0]] + " (" + str(pos[0]) + " " + star + ")"
	if lang == "Espanol":
		msg = "Los mejor valorados son " + first.encode('utf-8')
	else:
		msg = "The best rated are " + first
	
	if len(prlist) > 1:
		second = ", "+ prlist[pos[1]] + " (" + str(pos[1]) + " " + star + ")"
		if lang == "Espanol":
			msg += second.encode('utf-8')
		else:
			msg += second	
	if len(prlist) > 2:
		third = prlist[pos[2]] + " (" + str(pos[2])+ " " + star + ")"
		if lang == "Espanol":
			msg += " y " + third.encode('utf-8') + ".\n"
		else:
			msg +=" and " + third + ".\n"	
		
	return msg	
	
def noSuperuser(lang):
	if lang == "Espanol":
		return "Lo siento, no estás autorizado para ver esto. "
	else:
		return "Sorry, you aren't allowed to see this."
		
def stats(lang, stats):
	if lang == "Espanol":
		text = "¡Bienvenido!\nEl total de usuarios son " + str(stats['totalUsers'])
		text += ".\nY " + str(stats['usersWeek']) + " usuarios han usado, al menos una vez, el bot durante los últimos siete días."
		text += "\n" + str(stats['placesRate']) + " locales han sido puntuados. Y los usuarios han mandado fotos de "+ str(stats['placesPhotos'])
		text += " establecimientos diferentes.\n" + str(stats['english']) + " personas usan el bot en inglés y " + str(stats['spanish'])
		text += " en castellano.\n " 
	else:
		text = "Welcome!\nTotal users are " + str(stats['totalUsers'])
		text += ".\nAnd " + str(stats['usersWeek']) + " users have used the bot, at least once, during the last seven days."
		text += "\n" + str(stats['placesRate']) + " locals have been rated. And users have sent photos of " + str(stats['placesPhotos'])
		text += " different establishments.\n" + str(stats['english']) + " people use the bot in English and " + str(stats['spanish'])
		text += " in Spanish.\n " 
	return text
	
def afterMap(lang):
	if lang == "Espanol":
		text = "¡Aquí lo tienes!\n"
		text += "¿Qué quieres hacer ahora?" 
	else:
		text = "Here it is!\n"
		text += "What do you want to do now?"
	return text

def loading(lang):
	if lang == "Espanol":
		return "Cargando"
	else:
		return "Loading"

def rkeyboard(lang):
	if lang == "Espanol":
		return ["<< Anterior", "Más >>", "Atrás"]
	else:
		return ["<< Previous", "More >>", "Back"]
