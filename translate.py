#-*. coding: utf-8 -*-
#authors: David Quesada López y Mateo García Fuentes

def location(lang){
	if lang == "Español":
		return "¡Comparte tu localización!"
	else:
		return "Share your location!"
}

def settings(lang){
	if lang == "Español":
		text = "Desde aquí puedes cambiar los ajustes de tu bot. En Escoge idioma tu puedes cambiar el idioma del bot. "
		text += "En Escoge parámetros puedes cambiar el radio de los establecimientos que quieres ir, si quieres "
		text += "el bot solo mostrará los locales que estén abiertos en el momento de la consulta."
	else:
		text = "From here you can change the bot's settings. On Choose language you can change the bot's language. "
		text += "On Choose parameters you can change the radius of the establishments you want to go to, if you want "
		text += "the bot show you only local that are open at the momment of the query."
		
	return text
}

def lookingFor(lang){
	if lang == "Español":
		return "¿Qué estás buscando?"
	else:
		return "What are you looking for?"
}

def photoRec(lang){
	if lang == "Español":
		return "¡Foto recibida, gracias! ¿Qué más quieres hacer?"
	else:
		return "Photo received, thanks! What else would you like to do?"
}

def chooseOne(lang){
	if lang == "Español":
		return "¡Escoge uno!\n"
	else:
		return "Choose one!\n"
}

def isv(lang){
	if lang == "Español":
		return " es "
	else:
		return " is "
}

def meters(lang){
	if lang == "Español":
		return " metros de ti. "
	else:
		return " meters from you. "
}

def rate(lang){
	if lang == "Español":
		return "Y la puntucación de los usuarios es "
	else:
		return "And the rate of our users are "
}

def noEstablish(lang){
	if lang == "Español":
		return "No hay establecimientos con esos parámetros"
	else:
		return "There aren't establishment with this parameters."
}

def langChanged(lang){
	if lang == "Español":
		return "Idioma cambiado"
	else:
		return "Language changed"
}


def whatWant(lang){
	if lang == "Español":
		return "¿Qué quieres hacer?"
	else:
		return "What do you want to do?"
}

def chooseLang(lang){
	if lang == "Español":
		return "Escoge tu idioma"
	else:
		return "Choose your language"
}

def choooseParam(lang){
	if lang == "Español":
		return "Escoge los parámetros de tu consulta (radio, abierto ahora, etc.):"
	else:
		return "Choose the parameters for your query (radius, open now, etc.)."
}

def choooseParam(lang){
	if lang == "Español":
		text = "Desde aquí puedes cambiar los ajustes del bot. En Escoge idioma puedes cambiar el idioma del bot. "
		text += "En Escoge los parámetros puedes cambiar el radio de los locales a los que quieres ir, si quieres "
		text += "el bot puede mostarte solo los establecimientos abiertos."
		return tex
	else:
		text = "From here you can change the bot's settings. On Choose language you can change the bot's language. "
		text += "On Choose parameters you can change the radius of the establishments you want to go to, if you want "
		text += "the bot can show only locals that are open."
		return text
}

def choooseDistance(lang){
	if lang == "Español":
		return "Escoge una de las distancias que quieres establecer como radio de los locales que estás buscando. La distancias está en metros"
	else:
		return "Choose one of the distances which you want to set as radius of the establishments that you are looking for. The distance is in meters"
}

def onlyOpen(lang){
	if lang == "Español":
		return "¿Sólo quieres ver establecimientos abiertos en el momento de la consulta?"
	else:
		return "Do you want to see only open establishments at the moment of the query?"
}

def howLocals(lang){
	if lang == "Español":
		return "¿Cuántos establecimientos quieres ver?"
	else:
		return "How many establishments do you want to see?"
}

def radiusChanged(lang){
	if lang == "Español":
		return "Radio cambiado"
	else:
		return "Radius changed"
}

def openChanged(lang){
	if lang == "Español":
		return "Opción sólo abierto cambiada"
	else:
		return "Only open option changed"
}

def languageChanged(lang){
	if lang == "Español":
		return "Idioma cambiado"
	else:
		return "Language changed"
}

def numberChanged(lang){
	if lang == "Español":
		return "Número de locales cambiado"
	else:
		return "Number of establishment changed"
}

def hereIts(lang){
	if lang == "Español":
		return "Aquí lo tienes"
	else:
		return "Here it is"
}

def yourRate(lang){
	if lang == "Español":
		return "Entonces ... ¿Cúal es tu puntuación?"
	else:
		return "So... What's your rate?",
}

def sendPhoto(lang){
	if lang == "Español":
		return "¡Envíanos una foto del lugar!"
	else:
		return "Send us a photo of the place!",
}
