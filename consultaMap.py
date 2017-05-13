#! /usr/bin/python
#-*. coding: utf-8 -*-
import pymongo
import random
from pymongo import MongoClient
from mpl_toolkits.basemap import Basemap
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import Image

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
	

for i in range(1000):
	lt.append(random.uniform(min(lt), max(lt)))	
	ln.append(random.uniform(min(ln), max(ln)))	

llcrnrlon, llcrnrlat, urcrnrlon, urcrnrlat= sizeMap(lt, ln, 0.005)
map = Basemap(llcrnrlon=llcrnrlon,llcrnrlat=llcrnrlat,urcrnrlon=urcrnrlon,urcrnrlat=urcrnrlat, epsg=5520)
map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)
x,y = map(ln, lt)
#map.plot(x, y, 'bo', markersize=5,zorder=None, markerfacecolor='#424FA4',markeredgecolor="none", alpha=0.33 )
map.plot(x, y, 'ro', markersize=5,markeredgecolor="none", alpha=0.33)




plt.savefig("out.png")

back = Image.open("out.png")
loc = Image.open('loc.png')

Image.alpha_composite(back, loc).save("test.png")
"""
back.paste(loc, (10,10), loc)
back.show()

x0, y0 = map(40.423623, -3.694575)
x1, y1 = map(41.443683, -4.714505)
extent = [10, 12, 36, 38]
map.imshow(plt.imread('loc.png'), origin="lower", extent = extent)
plt.show()


x_size, y_size = 0.8, 0.4
x0, y0 = map(x[-1] - x_size/2., y[-1] - y_size/2.)
x1, y1 = map(x[-1] + x_size/2., y[-1] + y_size/2.)
im = plt.imshow(plt.imread('loc.png'), extent=(0, 0, 0, 0))

plt.savefig("out.png")

loc = img.imread("out.png")
plt.imshow(loc)
imgplot.plot """

"""
def puntos(a):
	for i in a: 
		if i != {}: 
			x, y = map(i['location']['longitude'],i['location']['latitude'])
			map.plot(x, y, marker='D',color='r')
"""
