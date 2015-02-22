from skimage import data
from skimage import io as io
from skimage.color import rgb2gray
from skimage.filter import gaussian_filter
import matplotlib.pyplot as plt
import sys
from skimage.feature import corner_fast, corner_peaks
from PIL import Image, ImageOps, ImageDraw
from skimage.util import img_as_ubyte
import numpy as np
import matplotlib.tri as tri
from scipy.spatial import Delaunay
from skimage.draw import polygon, set_color
from random import randint, uniform
from matplotlib.collections import PatchCollection

def process(file,blur,detail,trialpha):
	img = Image.open(file)
	img = ImageOps.expand(img,border=20,fill='white')
	img = ImageOps.expand(img,border=5,fill='black')
	w, h = img.size

	source = img_as_ubyte(img)
	img1 = rgb2gray(source)

	fig, ax = plt.subplots()
	plt.gray()

	# smaller means more detail
	if (blur > 0):
		img1 = gaussian_filter(img1, sigma=blur, multichannel=True)
		
	# corner_fast (more detail)
	corners = corner_peaks(corner_fast(img1, detail), min_distance=1)
	
	pts = np.zeros((len(corners),2))
	pts[:,0] = corners[:, 1]
	pts[:,1] = corners[:, 0]

	triangles = Delaunay(pts)
	triang = tri.Triangulation(corners[:, 1],corners[:, 0])

	centers = np.sum(pts[triangles.vertices], axis=1, dtype='int')/3.0

	pix = img.load()
	colors = []
	for i in centers:
		colors.append(pix[i[0],i[1]])

	ax.imshow(source)
	ax.axis('off')
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	patches = []

	for i in triangles.vertices:
		triangle = pts[i]
		a = triangle[0]
		b = triangle[1]
		c = triangle[2]
		triangle_center_x = (a[0] + b[0] + c[0]) * 0.33333
		triangle_center_y = (a[1] + b[1] + c[1]) * 0.33333
		colors = pix[triangle_center_x,triangle_center_y]
		# handle greyscale (or convert to RGB first)
		if isinstance(colors,int):
			R = colors / 255.
			G = colors / 255.
			B = colors / 255.
		else:
			R = colors[0] / 255.
			G = colors[1] / 255.
			B = colors[2] / 255.
		color = [R,G,B]
		y = np.array([a[1],b[1],c[1]])
		x = np.array([a[0],b[0],c[0]])
		polygon = plt.Polygon(triangle, fill=True, color=color, alpha=trialpha, ec='none', aa=True)
		patches.append(polygon)
		plt.gca().add_patch(polygon)

	plt.show()

# go (file, blur, detail, trialpha)
#
# a larger blur means less detail
# a smaller detail number means more detail
# setting trialpha to less than 1 means some of the source image will show

process(sys.argv[1],0,4,1)