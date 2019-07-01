# Import fastkml library
from fastkml import kml, styles, geometry
# Import Shapely library used by fastkml to create geometries
from shapely.geometry import Point, LineString, Polygon

# Import numpy to work with arrays
import numpy as np
# Import matplotlib to work with colormaps, and hex/rgb colors
from matplotlib import cm, colors

#function to make an aeroglyph were the color of each point is associated with a magnitude 'f'. 
def colorizedGlyph(data, folderPath, docname, nbins, limits, cmap_type):
	# data: a numpy matrix with [latitude, longitude, height, f] in each row. Where f is the variable asociated with the color.
	# folderPath: a string with the folder path
	# nbins: number of beans of the color map
	# limits: a list [min, max] which are the limits of our color scale.
	# cmap_type: a string with the name of the colormap. Read matplotlib.cm reference for further information.
	
	 
	colormap = cm.get_cmap(cmap_type, nbins)
	
	
	# Create the root KML object
	k = kml.KML()
	ns = '{http://www.opengis.net/kml/2.2}'

	# Create a KML Document and add it to the KML root object
	docid=''
	docdescription='This file was generated automaticaly with fastKML to colorize the aeroglyph.'
	kdoc = kml.Document(ns, docid, docname, docdescription)
	k.append(kdoc)
	
	# Create a KML Folder and add it to the Document
	folder1 = kml.Folder(ns, '', 'aeroglyph', '')
	kdoc.append(folder1)
	
	
	puntoPrev=[]
	idPunto=0
	for punto in data:
		if(idPunto!=0):
			u=(punto[3]-limits[0])/(limits[1]-limits[0])
			uprev=(puntoPrev[3]-limits[0])/(limits[1]-limits[0])
			u=(u+uprev)/2
			
			rgbcolor=colormap(u)
			
			hexcolor=colors.to_hex(rgbcolor, keep_alpha=True)
			hexcolor=hexcolor[-2:]+hexcolor[1:7]
			

			# Create a Placemark with a LineString geometry and add it to the Document
			estilolinea = styles.LineStyle(ns, color=hexcolor, width=4)
			estilo = styles.Style(styles=[estilolinea])
			p = kml.Placemark(ns, str(idPunto), styles=[estilo])
			p.geometry =  LineString([puntoPrev[0:3], punto[0:3]])
			# _geometry attribute is supposed not to be accessed directly
			# we have to look for a better solution using fastkml functions.
			p._geometry.altitude_mode='absolute'
			folder1.append(p)
			
		puntoPrev=punto
		idPunto+=1
	
	# write kml buffer to our file.
	fileHandle= open(folderPath+docname+'.kml',"w+")
	fileHandle.write(k.to_string(prettyprint=True))
	fileHandle.close()
