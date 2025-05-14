import dearpygui.dearpygui as dpg

# import our own image_class
from image_class import BaseImage
# make child class
class MyImageClass(BaseImage):
	# use: create object with: img_object = MyImageClass(width, height, channel, data)
	# where widht, height etc come from DearPyGui: width, height, channels, imagedata = dpg.load_image(path_to_file)

	# methods for filtering the image
	def some_filter_example(self):
		# always get the pixels from a copy, so you change the original
		copy_of_pixels = self.get_copy()
		# iterate over rows (top to bottom of the image)
		for rownr in range(self.h):
			# iterate over pixels (left to right in row y of image)
			for pixelnr in range(self.w):
				# pixel is an object of the Pixel class
				pixel = copy_of_pixels[rownr][pixelnr]

				# TODO --- THIS is where the filtering of this pixel takes place
				# remember red
				red = pixel.get_red()
				# red becomes green
				pixel.set_red(pixel.get_green())
				# green becomes blue
				pixel.set_green(pixel.get_blue())
				# blue becomes red
				pixel.set_blue(red)
				# TODO --- END of filtering of this pixel

				# put pixel back in original image
				self.pixels[rownr][pixelnr] = pixel
		return # ready


def main_window():
	# STARTING DPG STUFF
	dpg.create_context()
	dpg.create_viewport(title="Image filters in DearPyGui", width=840, height=660)
	dpg.setup_dearpygui()


	# TODO start
	# make a window in the main window
	window_tag = "my_image_window"  # the unique id of this window
	with dpg.window(label="The image", width=320, height=400, tag=window_tag):
		pass
	# you can add stuff to this window later, like an image

	# load image
	imagepath = "chrysi.png"
	width, height, channels, data = dpg.load_image(imagepath)
	# make it a MyImageClass object
	im = MyImageClass(width, height, channels, data)
	# apply the filter
	im.some_filter_example()
	# get changed data after filtering
	data = im.get_data()
	# then place image in texture (canvas)
	with dpg.texture_registry():
		texture_id = dpg.add_static_texture(width, height, data)

	# use the window_tag to put this texture in a specific window
	dpg.add_image(texture_id, parent=window_tag)
	# END TODO


	# RUNNING THE MAIN LOOP OF dpg
	dpg.show_viewport()
	dpg.start_dearpygui()
	# end of window
	dpg.destroy_context()

if __name__ == '__main__':
	main_window()
