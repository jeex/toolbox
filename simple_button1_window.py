import dearpygui.dearpygui as dpg

def open_new_window():
	print("Button clicked")
	
	with dpg.window(
			label="Second window", 
			width=320, 
			height=400, 
			tag="second window",
			pos=(330, 0),
		):
		pass
	
	# load image
	imagepath = "chrysi.png"
	width, height, channels, data = dpg.load_image(imagepath)

	# add image to texture (paint it on a canvas)
	with dpg.texture_registry():
		texture_id = dpg.add_static_texture(width, height, data)

	# use the window_tag to put this texture in a specific window
	dpg.add_image(texture_id, parent="second window")
	
	# TODO make button not work a second time
	
	

def main_window():
	dpg.create_context()
	dpg.create_viewport(
		title="Images in DearPyGui", # title in main window
		width=840, 
		height=660,
		x_pos=100,
		y_pos=100,
		resizable=False,
	)
	dpg.setup_dearpygui()

	# make a window in the main window
	window_tag = "my_image_window" # the unique id of this window
	with dpg.window(
			label="The image", 
			width=320, 
			height=400, 
			tag=window_tag,
			no_collapse=True,
			no_move=True,
			no_resize=True,
			no_close=True,
		):
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


	# TODO
	dpg.add_button(
		label="Another Window",
		tag="window_button",
		width=140,
		height=30,
		show=True,
		user_data=None,
		callback=open_new_window,
		parent=window_tag,
	)
	

	dpg.show_viewport()
	dpg.start_dearpygui()
	# end of window
	dpg.destroy_context()

if __name__ == '__main__':
	main_window()
