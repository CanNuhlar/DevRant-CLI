# got this code snipper from: http://code.activestate.com/recipes/580702-image-to-ascii-art-converter/

# ASCII Art Generator (Image to ASCII Art Converter)
# FB - 20160925
from __future__ import print_function
import sys,urllib, cStringIO




from PIL import Image, ImageDraw, ImageFont
font = ImageFont.load_default() # load default bitmap monospaced font
(chrx, chry) = font.getsize(chr(32))
# calculate weights of ASCII chars
weights = []
for i in range(32, 127):
    chrImage = font.getmask(chr(i))
    ctr = 0
    for y in range(chry):
        for x in range(chrx):
            if chrImage.getpixel((x, y)) > 0:
                ctr += 1
    weights.append(float(ctr) / (chrx * chry))


def print_ascii_from_url(img_url):

	file = cStringIO.StringIO(urllib.urlopen(img_url).read())
	image = Image.open(file)
	(imgx, imgy) = image.size
	imgx = int(imgx / chrx)
	imgy = int(imgy / chry)
	# NEAREST/BILINEAR/BICUBIC/ANTIALIAS
	image = image.resize((imgx, imgy), Image.BICUBIC)
	image = image.convert("L") # convert to grayscale
	pixels = image.load()
	
	for y in range(imgy):
    		for x in range(imgx):
        		w = float(pixels[x, y]) / 255
        		# find closest weight match
        		wf = -1.0; k = -1
        		for i in range(len(weights)):
            			if abs(weights[i] - w) <= abs(wf - w):
                			wf = weights[i]; k = i
        		print(chr(k + 32), end='')
    		print("")
	

#print_ascii_from_url("https://img.devrant.io/devrant/rant/r_378125_oGD4P.jpg")
