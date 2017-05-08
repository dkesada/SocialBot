import pymongo
from pymongo import MongoClient
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt

connection = MongoClient('localhost', 27017)

db = connection.bot

a = db.users.find({},{'_id':0,'location':1})

def puntos(a):
	for i in a: 
		if i != {}: 
			x, y = map(i['location']['longitude'],i['location']['latitude'])
			map.plot(x, y, marker='D',color='r')



map = Basemap(llcrnrlon=-10.5,llcrnrlat=35,urcrnrlon=4,urcrnrlat=45, epsg=5520)

map.arcgisimage(service='ESRI_Imagery_World_2D', xpixels = 1500, verbose= True)

puntos(a)

plt.show()
