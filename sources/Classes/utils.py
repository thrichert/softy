import sys, os

def resource_path(relative_path, oneFile):
	if oneFile:
		try:
			# PyInstaller creates a temp folder and stores path in _MEIPASS
			base_path = sys._MEIPASS
		except Exception:
			base_path = os.path.abspath(".")
	else:
		if getattr(sys, 'frozen', False):
			base_path = os.path.dirname(sys.executable)
		elif __file__:
			base_path = os.path.abspath('.')

	return os.path.join(base_path, relative_path)
