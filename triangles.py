import sys
import os.path
import matplotlib.pyplot as plt
import matplotlib.tri as mtri
import matplotlib.colors as matcolors
import matplotlib.cm as cmx
from matplotlib.collections import PatchCollection
import numpy as np
from skimage import io
from skimage.color import rgb2gray
from skimage.draw import polygon, set_color
from skimage.feature import corner_fast, corner_peaks
from skimage.filter import gaussian_filter
from skimage.util import img_as_ubyte
from PIL import Image, ImageOps, ImageDraw, ImageFilter
from scipy.spatial import Delaunay
from poisson.poisson_disk import sample_poisson_uniform

def tint_image(src, color="#FFFFFF"):
    src.load()
    r, g, b = src.split()
    gray = ImageOps.grayscale(src)
    result = ImageOps.colorize(gray, (0, 0, 0, 0), color) 
    return result

def process(**kwargs):
	# set default arguments
	file = kwargs.pop('file', "")
	append = kwargs.pop('append', "lp")
	blur = kwargs.pop('blur', 0)
	detail = kwargs.pop('detail', 1)
	size = kwargs.pop('size', 1)
	trialpha = kwargs.pop('trialpha', 1)
	random = kwargs.pop('random', False)
	
	# open the source image
	img = Image.open(file)
	img = ImageOps.expand(img,border=20,fill='white')
	img = ImageOps.expand(img,border=5,fill='black')
	w, h = img.size

	# uncomment to sharpen image (more points)
	#img = img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=3))
	#img.show()
	#exit()

	source = img_as_ubyte(img)
	img1 = rgb2gray(source)

	fig, ax = plt.subplots()
	plt.gray()

	# POINT EXTRACTION TWEAKS
	
	# blur image (fewer points)
	if (blur > 0):
		img1 = gaussian_filter(img1, sigma=blur, multichannel=True)

	# extract or generate points
	if (random):
		corners = sample_poisson_uniform(w,h,size,30)
		pts = np.zeros((len(corners),2))
		for i in range(len(corners)):
			x, y = corners[i]
			pts[i] = [int(x), int(y)]
	else:
		corners = corner_peaks(corner_fast(img1, detail), min_distance=size)
		pts = np.zeros((len(corners),2))
		pts[:,0] = corners[:, 1]
		pts[:,1] = corners[:, 0]
	
	triangles = Delaunay(pts)
	
	# COLOR SELECTION TWEAKS
	
	# tint image
	#img = tint_image(img,"#FF0000")
	
	# posterize image
	#img = ImageOps.posterize(img,4)
	
	# blur image
	#img = img.filter(ImageFilter.GaussianBlur(radius=10))
	
	pix = img.load()
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
		patches.append(plt.Polygon(triangle, fill=True, color=color, alpha=trialpha, ec='none', aa=True))

	ax.imshow(source)
	ax.axis('off')
	ax.axes.get_xaxis().set_visible(False)
	ax.axes.get_yaxis().set_visible(False)

	p = PatchCollection(patches, match_original=True)
	ax.add_collection(p)

	# plot extracted points
	#ax.scatter(pts[:,0], pts[:,1], s=1, color='g', alpha=1)
	#plt.show()
	
	# new file name
	name = os.path.splitext(file)[0]
	newname = name + '_' + append + '.png'
	
	# save + open file
	plt.savefig(newname, dpi=170, bbox_inches='tight', pad_inches = 0)
	command = "open " + newname
	os.system(command)

# append is a string to append to the end of the file when saving
# a larger blur means less detail to extract points from
# a smaller detail number means more extracted points
# a smaller size number means smaller triangles
# setting trialpha to less than 1 means some of the source image will show
file = sys.argv[1]
process(file=file, append="lp", blur=0, detail=1, size=1, trialpha=1, random=False)