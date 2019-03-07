import csv
from pyproj import Proj, transform, Geod
from PIL import Image, ImageFilter, ImageFont, ImageDraw
import time
import pymunk
from pymunk import Vec2d
import random
import geocoder
import pickle
import shapely
from shapely.geometry import LineString
import numpy as np

font = '/fonts/Akkurat/AkkRg_Pro.otf'
font = '/fonts/Gill/Gill Sans MT Pro Light.otf'
im = Image.open("maps/RobinsonWorld.png").convert('RGBA')
w,h = im.size
tmp = Image.new('RGBA', im.size, (0,0,0,0))

tailleMini = .003  # taille du texte en poucentage de la hauteur de la carte
tailleMaxi = .02 # taille du texte en poucentage de la hauteur de la carte
tailleMini = int(tailleMini * h)
tailleMaxi = int(tailleMaxi * h)

reduction = 10

def rescale(val, in_min, in_max, out_min, out_max):
	return out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))

def column(matrix, i):
	return [row[i] for row in matrix]

csvfile = open('data/test.csv', encoding='utf8')
results = csv.reader(csvfile, delimiter=';', quotechar='"')
results = list(results)

try:
	coord = pickle.load(open("coord.p", "rb" ) )
except:
	coord = {}

for i in results:
	try:
		coord[i[0]]
	except:
		if i[0] == 'Kazakhastan':
			i[0] = 'Kazakhstan'
		if i[0] == 'Letonnie':
			i[0] = 'Letonie'
		g = geocoder.osm(i[0])
		ll = g.latlng
		coord[i[0]] = ll

pickle.dump(coord, open("coord.p", "wb" ) )

liens = []

c = 0
for i in results:
	if c > 0:
		ll = coord[i[0]]
		if ll[0] not in column(liens,1) and ll[1] not in column(liens,2):
			liens.append([i[0], ll[0],ll[1],int(i[1]),int(i[2])])
		else:
			for j in liens:
				if i[0] + " " + i[0] == j[0]:
					j[4] += 1
	c += 1
	
mini, maxi = 100000,0
for i in liens:
	if i[3]+i[4] < mini:
		mini = i[3]+i[4]
	if i[3]+i[4] > maxi:
			maxi = i[3]+i[4]

inProj = Proj(init='EPSG:4326')
outProj = Proj('+proj=robin +lon_0=0 +lat_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs')

origLng,origLat = -transform(inProj,outProj,-180,0)[0], -transform(inProj,outProj,0,90)[1]

colors = [(242, 38, 19, 100),(242, 38, 19, 255),(30, 130, 76, 155)]

img = im.convert('RGBA')

cc = 0
for i in liens:
	print(cc,len(liens))
	tmp = Image.new('RGBA', im.size, (0,0,0,0))
	cc += 1
	g = Geod(ellps='WGS84')
	startlong, startlat, endlong, endlat = -73.5673,45.5017,i[2],i[1]
	(az12, az21, dist) = g.inv(startlong, startlat, endlong, endlat)
	lonlats = g.npts(startlong, startlat, endlong, endlat,
	                 1 + int(dist / 50000))
	lonlats.insert(0, (startlong, startlat))
	lonlats.append((endlong, endlat))
	c = 0
	for ll in lonlats:
		if c > 0:
			x,y = transform(inProj,outProj,ll[0],ll[1])
			
			x0C = int((x0 + origLng) * (w/(2*origLng)))
			y0C = int((y0 + origLat) * (h/(2*origLat)))
			
			xC = int((x + origLng) * (w/(2*origLng)))
			yC = int((y + origLat) * (h/(2*origLat)))
			
			if abs(x0C - xC) < 1633:
#				draw = ImageDraw.Draw(img, 'RGBA')
				draw = ImageDraw.Draw(tmp)
#				color = (44, 130, 201,155)
				largeur = int(rescale(i[3]+i[4], mini, maxi, tailleMini, tailleMaxi)/4)
#				print(mini, maxi,np.logspace(mini, maxi, num=10, endpoint=True, base=2.0))
				width = int((tailleMini / 5) + 2 * (c/len(lonlats)*largeur))
				
				bicolor = False
				if bicolor:
					# séparation de lignes
					line1 = LineString([(x0C, y0C), (xC, yC)]).parallel_offset(width/4,'left')
					line2 = LineString([(x0C, y0C), (xC, yC)]).parallel_offset(width/4,'right')
					draw.line((line1.coords[0][0],line1.coords[0][1],line1.coords[1][0],line1.coords[1][1]), fill=colors[0], width = int(.5 * width))
					draw.line((line2.coords[0][0],line2.coords[0][1],line2.coords[1][0],line2.coords[1][1]), fill=colors[1], width = int(.5 * width))
				else:
					draw.line((x0C,y0C,xC,yC), fill=colors[0], width = width)
			
		x0,y0 = transform(inProj,outProj,ll[0],ll[1])
		c += 1
	img = Image.alpha_composite(img, tmp)

space = pymunk.Space()
space.gravity = (0.0, 0.0)
balls = []
bodies = []
for l in liens:
	x,y = transform(inProj,outProj,l[2],l[1])
	x = int((x + origLng) * (w/(2*origLng)))
	y = int((y + origLat) * (h/(2*origLat)))
	l[1] = x
	l[2] = y
	mass = 1
	radius = int(rescale(l[3]+l[4], mini, maxi, tailleMini, tailleMaxi))
	inertia = pymunk.moment_for_circle(mass, 0, radius, (0,0))
	body = pymunk.Body(mass, inertia)
	body.position = x,y
	body.positionOld = x,y
	body.info = l[0]
	body.positionOrigin = x,y
	shape = pymunk.Circle(body, radius, Vec2d(0,0))
	space.add(body, shape)
	balls.append(shape)
	bodies.append(body)

for i in range(100):
	space.step(0.02)

for b in bodies:
	for l in liens:
		if l[0] == b.info:
			l.append(b.position)

physics = True

for i in liens:
	texte = str(i[3]+i[4])
	taille = int(rescale(i[3]+i[4], mini, maxi, tailleMini, tailleMaxi))
	t = 1
	fnt = ImageFont.truetype(font, t)
	while max(draw.textsize(texte, font=fnt)[0],draw.textsize(texte, font=fnt)[1]) < taille * 2:
		t += 1
		fnt = ImageFont.truetype(font, int(t))
	t -= 1
	t *= .75
	fnt = ImageFont.truetype(font, int(t))
#	print(texte,taille)
#	print(texte,draw.textsize(texte, font=fnt)[0])
	if physics:
		x1,y1 = i[5][0],i[5][1]
	else:
		x1,y1 = i[1],i[2]
#	draw = ImageDraw.Draw(img, 'RGBA')
#	draw = ImageDraw.Draw(tmp)
				
	draw.ellipse((x1 - taille -5, y1 - taille -5, x1 + taille +5, y1 + taille +5), fill = (255,255,255,127))
	draw.ellipse((x1 - taille, y1 - taille, x1 + taille, y1 + taille), fill = colors[1])
	
	offsetX = int(float(draw.textsize(texte, font=fnt)[0])/2)
	offsetY = int(float(draw.textsize(texte, font=fnt)[1])/2)
	draw.text((x1 - offsetX,y1 - offsetY), texte, font=fnt, fill=(255,255,255,255))

img = Image.alpha_composite(img, tmp)
img = img.convert("RGB") # Remove alpha for saving in jpg format.

img.save('result.png')
