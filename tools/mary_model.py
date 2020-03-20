class MaryModel():

	def fill(self, *args, **kwargs):

		for key, value in kwargs.items():
			setattr(self, key, value)
