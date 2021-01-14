from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json

from Classes.DB import DB
from Classes.MainWindow import MainWindow

from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

def resource_path(relative_path):
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")
	return os.path.join(base_path, relative_path)


if __name__ == "__main__":

	# init DB
	database = DB()
	# TODO archive Db if 1 day since last save
	database.saveDb()

	# TODO check data consistency

	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow(database)
	app.exec_()


