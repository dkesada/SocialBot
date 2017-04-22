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
