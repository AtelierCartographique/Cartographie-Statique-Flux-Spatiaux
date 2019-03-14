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
import math
import seaborn as sns
import time

font = 'fonts/Akkurat/AkkLg_Pro.otf'
font = 'fonts/Akkurat/AkkRg_Pro.otf'
font2 = 'fonts/Akkurat/AkkRg_Pro.otf'
font3 = 'fonts/Akkurat/AkkBd_Pro.ttf'
im = Image.open("maps/RobinsonWorld.png").convert('RGBA')
w,h = im.size
data = 'data/NFootprint-Reasons_travel_EN.csv'
data = 'data/NFootprint_etudiants_EN.csv'
colors = [(100, 100, 100, 50),(100, 100, 100, 0),(30, 130, 76, 255),(214, 69, 65, 255),(115, 101, 152, 255),(82, 179, 217, 255),(46, 204, 113, 255),(255, 236, 139, 255),(252, 185, 65, 255)]

datas = [['data/NFootprint-Reasons_travel_EN.csv','Reason of travel','Total number of travels'],['data/NFootprint_etudiants_EN.csv','Origin of student','Total number of students']]
palettes = ['Set1','Set2','Dark2','Accent']
palettes = ['Dark2']
logs = [0]
tailles = [[0.01,0.05],[0.008,0.04],[0.005,0.03]]
for data in datas:
	for palette in palettes:
		for log in logs:
			for taille in tailles:
				t0 = time.time()

				paletteQualit = []
				for rgb in sns.color_palette(palette):
					rgb = (int(rgb[0]*255),int(rgb[1]*255),int(rgb[2]*255))
					paletteQualit.append((rgb[0],rgb[1],rgb[2]))

				opacityPies = 50 
				physics = True
				#log = 0


				img = im.convert('RGBA')
				tmp = Image.new('RGBA', im.size, (0,0,0,0))

				tailleMini = taille[0]#.005  # taille du texte en poucentage de la hauteur de la carte
				tailleMaxi = taille[1]#.03 # taille du texte en poucentage de la hauteur de la carte

				tailleMini = int(tailleMini * h)
				tailleMaxi = int(tailleMaxi * h)

				reduction =  0

				def legend(l,paletteQualit,mini, maxi, tailleMini, tailleMaxi, titleColors = data[1],titleSizes = data[2]):
				#	print(l)
					margin = 100
					marginText = margin * .5
					nbr_keys = 6
					legendTextSize = int(h/75)
					legendTitleSize = int(legendTextSize * 1)
					spaceBetweenLegends = legendTextSize * 2
					spaceBetweenlegendTexts = legendTextSize * 1.8
					coordinates = []
					
					l.pop(0)
					l.reverse()
					
					draw = ImageDraw.Draw(img, 'RGBA')
					
					# Couleurs
					c = 0
					for ll in range(len(l)):
								
						rayon = legendTextSize / 2
						
						texte = l[ll]
						
						xCouleur = margin + rayon
						yCouleur = h - margin - rayon - ll * spaceBetweenlegendTexts
						
						xTexte = margin + 2 * rayon + marginText
						yTexte = h - margin - rayon - ll * spaceBetweenlegendTexts
						
						col = paletteQualit[len(l)-c-1]
				#		print(texte,col,l)
						c += 1
						
						coordinates.append([[xCouleur, yCouleur],[xTexte, yTexte],texte,"fonts/Akkurat/AkkRg_Pro.otf",legendTextSize,'color',rayon,col])
					
					# Titre couleurs
					xTitre = xCouleur - rayon
					yTitre = yTexte - legendTextSize * 2
					coordinates.append([[xCouleur, yCouleur],[xTitre, yTitre],titleColors.upper(),"fonts/Akkurat/AkkBd_Pro.ttf",legendTitleSize,'title'])
					
					# Tailles
					yCircle = yTitre - spaceBetweenLegends
					offset = 0
					for k in range(nbr_keys + 1):
						
						rayon = rescale(mini + k * (maxi-mini)/nbr_keys, mini, maxi, tailleMini, tailleMaxi, log)
						
						texte = str(mini + k * (maxi-mini)/nbr_keys).split('.')[0]
						if maxi-mini <= 100:
							base = 5
						elif maxi-mini <= 1000:
							base = 50
						elif maxi-mini <= 10000:
							base = 500
							
						rayon = int(base * round(rescale(mini + k * (maxi-mini)/nbr_keys, mini, maxi, tailleMini, tailleMaxi, log))/base)
						texte = str(int(base * round(float(mini + k * (maxi-mini)/nbr_keys)/base)))
						if texte == "0":
							texte = "1"
						#rayonMax = rescale(maxi, mini, maxi, tailleMini, tailleMaxi, log)
						rayonMax = int(base * round(rescale(maxi, mini, maxi, tailleMini, tailleMaxi, log))/base)
						print(texte,rayonMax)
						
						xCircle = margin + rayonMax
						yCircle -= offset + rayon + spaceBetweenlegendTexts/5
								
						xTexte = margin + rayonMax + rayon + marginText
						yTexte = yCircle
						
						coordinates.append([[xCircle, yCircle],[xTexte, yTexte],texte,"fonts/Akkurat/AkkRg_Pro.otf",legendTextSize,'size',rayon])
						
						offset = rayon
					
					# Titre tailles
					yTitre = yTexte - legendTextSize - rayon
					if log == 0:
						texte = titleSizes.upper()
					else:
						texte = titleSizes.upper() + " (base-" + str(log) + " log scale)"
						
					coordinates.append([[xCouleur, yCouleur],[xTitre, yTitre],texte.upper(),"fonts/Akkurat/AkkBd_Pro.ttf",legendTitleSize,'title'])
					
					# dessin de la légende
					c = 0
					for elem in coordinates:
						fnt = ImageFont.truetype(elem[3], elem[4])
						if elem[5] == 'color':
							rayon = elem[6]
							col = elem[7]
							draw.ellipse((elem[0][0] - rayon - 5, elem[0][1] - rayon - 5, elem[0][0] + rayon + 5, elem[0][1] + rayon + 5), fill = col)
							c += 1
						
						if elem[5] == 'size':
							rayon = elem[6]
							draw.ellipse((elem[0][0] - rayon, elem[0][1] - rayon, elem[0][0] + rayon, elem[0][1] + rayon), fill = (50,50,50,255))		
							draw.ellipse((elem[0][0] - rayon + 5, elem[0][1] - rayon + 5, elem[0][0] + rayon - 5, elem[0][1] + rayon - 5), fill = (255,255,255,255))
						
						draw.text((elem[1][0], elem[1][1] - draw.textsize(texte, font=fnt)[1] / 2), elem[2], font=fnt, fill=(0,0,0,255))

				def pol2cart(rho, phi):
					x = rho * np.cos(phi)
					y = rho * np.sin(phi)
					return(x, y)

				def camembert(x1,y1,v,r):
					
					angle_old = 0
					c = 0

					for i in v[3]:
						if i != 0:
							polygon = [(x1,y1),(x1 + pol2cart(r,angle_old - math.pi / 2)[0],y1 + pol2cart(r,angle_old - math.pi / 2)[1])]

							angle = 2 * math.pi * float(i) / sum(v[3])			
							detailCercle = 100
							for p in range(detailCercle):
								polygon.append((x1 + pol2cart(r,angle_old + angle/detailCercle*p - math.pi / 2)[0],y1 + pol2cart(r,angle_old + angle/detailCercle*p - math.pi / 2)[1]))

							polygon.append((x1 + pol2cart(r,angle_old + angle - math.pi / 2)[0],y1 + pol2cart(r,angle_old + angle - math.pi / 2)[1]))
							angle_old += 2 * math.pi * float(i) / sum(v[3])
							draw.polygon(polygon,fill=paletteQualit[c])
						c += 1
						if c == 9:
							break

				def rescale(val, in_min, in_max, out_min, out_max, log):
					if log > 1:
						in_min = math.log(in_min,log)
						in_max = math.log(in_max,log)
						val = math.log(val,log)
					area = out_min + (val - in_min) * ((out_max - out_min) / (in_max - in_min))
					radius = math.sqrt(area/math.pi)
					return area

				def column(matrix, i):
					return [row[i] for row in matrix]

				csvfile = open(data[0], encoding='utf8')
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
						if type(i[0]) is not tuple:
							g = geocoder.osm(i[0])
							ll = g.latlng
							coord[i[0]] = ll

				pickle.dump(coord, open("coord.p", "wb" ))

				liens = []

				c = 0
				for i in results:
					if c > 0:
						if type(i[0]) is not tuple:
							ll = coord[i[0]]
						else:
							ll = i[0]
						if ll[0] not in column(liens,1) and ll[1] not in column(liens,2):
				#			liens.append([i[0], ll[0],ll[1],int(i[1]),int(i[2])])
							val = []
							cc = 0
							for ii in i:
								if cc != 0:
									val.append(int(ii))
								cc += 1
							liens.append([i[0], ll[0],ll[1],val])
						else:
							for j in liens:
								if i[0] + " " + i[0] == j[0]:
									j[4] += 1
					c += 1
					
				mini, maxi = 100000,0
				for i in liens:
					if sum(i[3]) < mini:
						mini = sum(i[3])
					if sum(i[3]) > maxi:
							maxi = sum(i[3])

				inProj = Proj(init='EPSG:4326')
				outProj = Proj('+proj=robin +lon_0=0 +lat_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +units=m +no_defs')

				origLng,origLat = -transform(inProj,outProj,-180,0)[0], -transform(inProj,outProj,0,90)[1]

				cc = 0
				for i in liens:
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
								largeur = int(rescale(sum(i[3]), mini, maxi, tailleMini, tailleMaxi, log)/4)
				#				print(mini, maxi,np.logspace(mini, maxi, num=10, endpoint=True, base=2.0))
								width = int((tailleMini / 5) + 2 * (c/len(lonlats)*largeur))
								
								bicolor = False
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
					radius = int(rescale(sum(l[3]), mini, maxi, tailleMini, tailleMaxi, log)) + 5
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

				for i in liens:
					texte = str(sum(i[3]))
					radius = int(rescale(sum(i[3]), mini, maxi, tailleMini, tailleMaxi, log))
					#radius = math.sqrt(area/math.pi)
					
					t = 1
					fnt = ImageFont.truetype(font, t)
					while max(draw.textsize(texte, font=fnt)[0],draw.textsize(texte, font=fnt)[1]) < radius * 2:
						t += 1
						fnt = ImageFont.truetype(font, int(t))
					t -= 1
					t *= .5
					fnt = ImageFont.truetype(font, int(t))
					if physics:
						x1,y1 = i[4][0],i[4][1]
					else:
						x1,y1 = i[1],i[2]
								
					draw.ellipse((x1 - radius -5, y1 - radius -5, x1 + radius +5, y1 + radius +5), fill = (255,255,255,127))
				#	draw.ellipse((x1 - taille, y1 - taille, x1 + taille, y1 + taille), fill = colors[1])
					camembert(x1,y1,i,radius)
					
					offsetX = int(float(draw.textsize(texte, font=fnt)[0])/2)
					offsetY = int(float(draw.textsize(texte, font=fnt)[1])/2)
				#	draw.text((x1 - offsetX,y1 - offsetY), texte, font=fnt, fill=(255,255,255,255))
				
				legend(results[0],paletteQualit,mini, maxi, tailleMini, tailleMaxi)
				
				img = Image.alpha_composite(img, tmp)
				img = img.convert("RGB") # Remove alpha for saving in jpg format.
				
				if log == 0:
					logS = 'Linear'
				else:
					logS = 'Log' + str(log)
				img.save('results/' + data[0].split('/')[1].replace('.csv','') + '_Size-' + str(taille[0]) + '-' + str(taille[1]) + '_Scale-' + logS + '_Palette-' + palette + '.jpg')
				
				print(time.time()-t0,data,palette,log,taille)
