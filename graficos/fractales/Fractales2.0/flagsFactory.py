class FlagsFactory:
	@staticmethod
	def crearFlags(**args):
		return type("Flags",(),args)