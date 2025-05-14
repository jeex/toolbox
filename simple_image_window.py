import dearpygui.dearpygui as dpg

def main_window():
	# STARTING DPG STUFF
	dpg.create_context()
	dpg.create_viewport(title="Images in DearPyGui", width=840, height=660)
	dpg.setup_dearpygui()

	# make a window in the main window
	window_tag = "my_image_window" # the unique id of this window
	with dpg.window(label="The image", width=320, height=400, tag=window_tag):
		pass
	# you can add stuff to this window later, like an image

	# load image
	imagepath = "chrysi.png"
	width, height, channels, data = dpg.load_image(imagepath)

	# add image to texture (paint it on a canvas)
	with dpg.texture_registry():
		texture_id = dpg.add_static_texture(width, height, data)

	# use the window_tag to put this texture in a specific window
	dpg.add_image(texture_id, parent=window_tag)

	dpg.show_viewport()
	dpg.start_dearpygui()
	# end of window
	dpg.destroy_context()

if __name__ == '__main__':
	main_window()
