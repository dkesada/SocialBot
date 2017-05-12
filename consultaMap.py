#! /usr/bin/python
#-*. coding: utf-8 -*-
import pymongo
from pymongo import MongoClient
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

connection = MongoClient('localhost', 27017)
db = connection.bot
a = db.users.find({},{'_id':0,'location':1})

def sizeMap(lats, longs, scale):

	northLat = max(lats)
	southLat = min(lats)
	westLon = max(longs)
	eastLon = min(longs)

	llcrnrlon = eastLon-scale
	llcrnrlat = southLat-scale

	urcrnrlon = westLon+scale
	urcrnrlat = northLat+scale

	return llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat

ln = []
lt = []
for geo in a:
	if geo != {}:
		ln.append(geo['location']['longitude'])
		lt.append(geo['location']['latitude'])		
	
llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat= sizeMap(lt, ln, 0.01)
map = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat, epsg=5520)
map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
x,y = map(ln, lt)
map.plot(x, y, 'bo', markersize=5)
plt.show()


"""
def puntos(a):
	for i in a: 
		if i != {}: 
			x, y = map(i['location']['longitude'],i['location']['latitude'])
			map.plot(x, y, marker='D',color='r')
"""
