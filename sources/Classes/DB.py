from PyQt5 import QtWidgets, QtCore, QtGui
import sys, os, json, platform, time

def resource_path(relative_path):
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)

class DB(object):

	__PATH_DIR_DB	= resource_path("./DataBase/")
	__PATH_BD		= resource_path("./DataBase/db.json")

	def __init__(self):
		self.path = DB.__PATH_BD
		now = QtCore.QDate().currentDate()

		if not os.path.exists(DB.__PATH_BD):
			self.data = {
				"lastDBsave": now.toString("dd.MM.yyyy"),
				"BUs":{},
				"IAs": {},
				"INGs": {},
				"archive":{
					"IAs":{},
					"INGs":{},
					"BUs":{}
				}
			}
			# create dir if not exist
			if not os.path.exists(DB.__PATH_DIR_DB):
				os.makedirs(DB.__PATH_DIR_DB)
			with open(DB.__PATH_BD, 'w') as f:
				f.write(json.dumps(self.data, sort_keys=True, indent=4))
		else:
			with open(DB.__PATH_BD, 'r') as f:
				self.data = json.load(f)

	def write(self, data):
		now = QtCore.QDate().currentDate()
		self.data = data
		self.data["lastDBsave"] = now.toString("dd.MM.yyyy")
		with open(self.path, 'w') as f:
			f.write(json.dumps(self.data, sort_keys=True, indent=4))

	def getContent(self):
		return self.data

	def saveDb(self):
		now = QtCore.QDate().currentDate()
		lastSave = QtCore.QDate().fromString(self.data["lastDBsave"], "dd.MM.yyyy")
		if now > lastSave:
			with open(DB.__PATH_DIR_DB + now.toString('yyyy_MM_dd_saveDB.json'), 'w') as f:
				f.write(json.dumps(self.data, sort_keys=True, indent=4))
		# remove current
		os.remove(self.path)
		# save new
		self.write(self.data)
		# remove previous saving older than a 2 day
		# folderContent = os.listdir(path)
		# for f in folderContent:
		# 	timestamp = self._creation_date(path + f)
		# 	now = time.time()
		# 	if ((now - timestamp)/60/60/24) > 2:
		# 		os.remove(path + f)

	def _creation_date(self, path_to_file):
		"""
		Try to get the date that a file was created, falling back to when it was
		last modified if that isn't possible.
		See http://stackoverflow.com/a/39501288/1709587 for explanation.
		"""
		if platform.system() == 'Windows':
			return os.path.getctime(path_to_file)
		else:
			stat = os.stat(path_to_file)
			try:
				return stat.st_birthtime
			except AttributeError:
				# We're probably on Linux. No easy way to get creation dates here,
				# so we'll settle for when its content was last modified.
				return stat.st_mtime