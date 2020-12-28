from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json

from Classes.DB import DB
from Classes.MainWindow import MainWindow

from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

if __name__ == "__main__":
	# init DB
	database = DB("./DataBase/db.json")
	# archive Db if 1 day since last save
	database.saveDb('./Database/')

	# check data consistency

	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow(database)
	app.exec_()