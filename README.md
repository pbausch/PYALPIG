# PYALPIG
A python script to generate a low-poly image from a photo.

usage: python triangles.py [image file]

I know nothing about Python. This is my first Python script. It uses [scikit-image](http://scikit-image.org/), [matplotlib](http://matplotlib.org/), and [shapely](https://pypi.python.org/pypi/Shapely) to generate Low Poly art similar to the app [PolyGen](http://www.polygenapp.com/).

The script extracts points from the picture, creates a Delaunay mesh, finds the center point of every triangle, extracts the color of that pixel, and then fills/plots that triangle with that color. You can optionally use a Voronoi diagram instead.

I put something like this together in JavaScript--[YALPIG](https://github.com/pbausch/YALPIG)--and wanted something similar on the command line. I thought Python might work well for it.

To Do:

 * It's fairly slow. PatchCollections help with plotting thousands of polygons, but I wonder if there's a way to parallelize somehow.
 * I'd like to make this interactive like the JavaScript version so I can fiddle with knobs to get different results. I have no idea how to do that.
 * Instead of getting the color of the pixel at the center of the triangle, I'd like to try averaging all pixels within a triangle and using that for the Polygon. Again, no idea how to get the coordinates of every pixel within a triangle.
 * I'd like to be able to find the foreground and background of an image and only create the mesh in one or the other.
