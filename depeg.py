import dearpygui.dearpygui as dpg
from image_class import BaseImage, Pixel

class MyFilters(BaseImage):
	# this is an example filter
	def filter_example(self):
		# always get the pixels from a copy, so you change the original
		copy_of_pixels = self.get_copy()

		# iterate over rows (top to bottom of the image)
		for rownr in range(self.h):
			# iterate over pixels (left to right in row y of image)
			for pixelnr in range(self.w):
				# pixel is an object of the Pixel class
				pixel = copy_of_pixels[rownr][pixelnr]

				# TODO manipulate pixel

				# MAKE color rotate:
				red = pixel.get_red()
				# red becomes green
				pixel.set_red(pixel.get_green())
				# green becomes blue
				pixel.set_green(pixel.get_blue())
				# blue becomes red
				pixel.set_blue(red)

				# put pixel back in original
				self.pixels[rownr][pixelnr] = pixel

	def filter_bw(self):
		# always get the pixels from a copy, so you change the original
		copy_of_pixels = self.get_copy()

		# iterate over rows (top to bottom of the image)
		for rownr in range(self.h):
			# iterate over pixels (left to right in row y of image)
			for pixelnr in range(self.w):
				# pixel is an object of the Pixel class
				pixel = copy_of_pixels[rownr][pixelnr]

				# manipulate pixel
				r = pixel.get_red()
				g = pixel.get_green()
				b = pixel.get_blue()
				if r + g + b > (3 * 256 / 2):
					r = g = b = 255
				else:
					r = g = b = 0
				pixel.set_red(r)
				pixel.set_green(g)
				pixel.set_blue(b)

				# put pixel back in original
				self.pixels[rownr][pixelnr] = pixel

	def filter_contrast(self, level=0.2):
		# always get the pixels from a copy, so you change the original
		copy_of_pixels = self.get_copy()

		# iterate over rows (top to bottom of the image)
		for rownr in range(self.h):
			# iterate over pixels (left to right in row y of image)
			for pixelnr in range(self.w):
				# pixel is an object of the Pixel class
				pixel = copy_of_pixels[rownr][pixelnr]

				# manipulate pixel
				r = pixel.get_red()
				g = pixel.get_green()
				b = pixel.get_blue()
				if r > 256 / 2:
					pixel.set_red(self.colorfit(r + r * level))
				else:
					pixel.set_red(self.colorfit(r - r * level))
				if g > 256 / 2:
					pixel.set_green(self.colorfit(g + g * level))
				else:
					pixel.set_green(self.colorfit(g - g * level))
				if b > 256 / 2:
					pixel.set_blue(self.colorfit(b + b * level))
				else:
					pixel.set_blue(self.colorfit(b - b * level))

				# put pixel back in original
				self.pixels[rownr][pixelnr] = pixel

	def filter_edge(self):
		from math import sqrt

		from copy import deepcopy
		copy_of_pixels = self.get_copy()
		gx = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
		gy = [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
		# get pixels from im
		# put pixels back in copy_im
		for rownr in range(self.h):
			for pixelnr in range(self.w):
				pixel = copy_of_pixels[rownr][pixelnr]

				gxBlue = 0
				gyBlue = 0
				gxGreen = 0
				gyGreen = 0
				gxRed = 0
				gyRed = 0

				for py in (-1, 0, 1):
					if py + rownr < 0 or py + rownr >= self.h:
						continue
					for px in range(-1, 0, 1):
						if px + pixelnr < 0 or px + pixelnr >= self.w:
							continue
						pp = copy_of_pixels[py + rownr][px + pixelnr]

						gxBlue += pp.get_blue() * gx[py + 1][px + 1]
						gyBlue += pp.get_blue() * gy[py + 1][px + 1]
						gxGreen += pp.get_green() * gx[py + 1][px + 1]
						gyGreen += pp.get_green() * gy[py + 1][px + 1]
						gxRed += pp.get_red() * gx[py + 1][px + 1]
						gyRed += pp.get_red() * gy[py + 1][px + 1]

				# klaar met pixel x, y
				bl = self.colorfit(sqrt((gxBlue * gxBlue) + (gyBlue * gyBlue)))
				gr = self.colorfit(sqrt((gxGreen * gxGreen) + (gyGreen * gyGreen)))
				rd = self.colorfit(sqrt((gxRed * gxRed) + (gyRed * gyRed)))
				pixel.set_red(rd)
				pixel.set_green(gr)
				pixel.set_blue(bl)

				self.pixels[rownr][pixelnr] = pixel


def make_window_image(width, height, mio):
	# add image to texture (sort of a canvas) using changed pixels from MyFilters object
	with dpg.texture_registry():
		texture_id = dpg.add_static_texture(width, height, mio.to_data())
	# make elements in window
	with dpg.window(label="Photo Filters"):
		# add stuff to the window
		dpg.add_image(texture_id)

# start stuff
dpg.create_context()
dpg.create_viewport(title="DePeg", width=640, height=660)
dpg.setup_dearpygui()

# load image 
try:
	width, height, channels, data = dpg.load_image("chrysi.png", gamma=1, gamma_scale_factor=1)
except:
	dpg.destroy_context()
	exit()

# manipulate data of image
mi = MyFilters(width, height, channels, data)
mi.filter_contrast(0.4)


make_window_image(width, height, mi)


# main loop
dpg.show_viewport()
while dpg.is_dearpygui_running():
	dpg.render_dearpygui_frame()

dpg.destroy_context()
