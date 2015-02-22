import sys
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from skimage import data
from skimage import io
from skimage.color import rgb2gray
from skimage.draw import polygon, set_color
from skimage.feature import corner_fast, corner_peaks
from skimage.filter import gaussian_filter
from skimage.util import img_as_ubyte
from PIL import Image, ImageOps, ImageDraw
from scipy.spatial import Delaunay

def process(file,blur,detail,trialpha):
	img = Image.open(file)
	img = ImageOps.expand(img,border=20,fill='white')
	img = ImageOps.expand(img,border=5,fill='black')
	w, h = img.size

	source = img_as_ubyte(img)
	img1 = rgb2gray(source)

	fig, ax = plt.subplots()
	plt.gray()

	if (blur > 0):
		img1 = gaussian_filter(img1, sigma=blur, multichannel=True)
		
	corners = corner_peaks(corner_fast(img1, detail), min_distance=1)
	
	pts = np.zeros((len(corners),2))
	pts[:,0] = corners[:, 1]
	pts[:,1] = corners[:, 0]
	
	# random points
	#pts = np.random.random_integers(w, size=(1000,2))
		
	triangles = Delaunay(pts)

	pix = img.load()

	ax.imshow(source)
	ax.axis('off')
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

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
		polygon = plt.Polygon(triangle, fill=True, color=color, alpha=trialpha, ec='none', aa=True)
		plt.gca().add_patch(polygon)

	# plot points
	#ax.scatter(pts[:,0], pts[:,1], s=1, color='g', alpha=1)
	plt.show()

# go (file, blur, detail, trialpha)
#
# a larger blur means less detail
# a smaller detail number means more detail
# setting trialpha to less than 1 means some of the source image will show

process(sys.argv[1],0,1,1)