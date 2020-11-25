from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.MainWindow import MainWindow


if __name__ == "__main__":
	# init DB
	database = DB("./DataBase/db.json")
	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow(database)
	app.exec_()