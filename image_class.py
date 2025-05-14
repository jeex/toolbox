from copy import deepcopy

class Pixel:
	r = 0
	g = 0
	b = 0
	a = None

	def __init__(self, r, g, b, a=None):
		self.r = r
		self.g = g
		self.b = b
		self.a = a

	def __str__(self):
		return f"({self.r}, {self.g}, {self.b}, {self.a})"

	def set_red(self, val):
		self.r = val
	def set_green(self, val):
		self.g = val
	def set_blue(self, val):
		self.b = val
	def set_alpha(self, val):
		self.a = val

	def get_red(self):
		return self.r
	def get_green(self):
		return self.g
	def get_blue(self):
		return self.b
	def get_alpha(self):
		return self.a

class BaseImage:
	def __init__(self, width, height, channels, data):
		self.w = width
		self.h = height
		self.has_alpha = channels == 4
		self.to_matrix(data)
		# print(self.has_alpha, len(self.pixels), len(self.pixels[0]))

	def to_matrix(self, data):
		# converts the list of data into a matrix with rows containing pixels
		self.pixels = list() # list of lists [row][column] with pixels
		y = 0
		i = 0
		while i < len(data):
			x = 0
			# single row
			row = list()
			while x < self.w:
				r = self.float_to_256(data[i])
				i += 1
				g = self.float_to_256(data[i])
				i += 1
				b = self.float_to_256(data[i])
				i += 1
				# with or without alpha channel
				if self.has_alpha:
					a = data[i]
					i += 1
				else:
					a = None
				# make pixel object
				pixel = Pixel(r, g, b, a)
				# add pixel to row
				row.append(pixel)
				x += 1
			# add row to matrixs of pixels
			y += 1
			self.pixels.append(row)

	def float_to_256(self, f: float):
		# recalculates value of 0 .. 1 to 0 .. 256
		return min(max(int(f * 256), 0), 255)

	def fit256(self, i):
		# makes int for color always fit
		return max(0, min(255, int(round(i))))

	def float_from_256(self, c):
		# recalculate to float
		return c / 256

	def get_data(self):
		# returns the matrix of pixels in list for DearPyGui use
		data = list()
		for row in self.pixels:
			for pixel in row:
				data.append(self.float_from_256(pixel.r))
				data.append(self.float_from_256(pixel.g))
				data.append(self.float_from_256(pixel.b))
				if self.has_alpha:
					data.append(pixel.a)
		return data

	def get_copy(self):
		# makes a deepcopy of the pixels matrix
		return deepcopy(self.pixels)
