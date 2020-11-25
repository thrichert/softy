from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.ING import ING

class Diag_addING_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Engineer
	"""
	def __init__(self, viewPath, database, mainWindow):
		super(Diag_addING_Window, self).__init__()
		uic.loadUi(viewPath,self)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			#check user input
			userName = self.findChild(QtWidgets.QLineEdit, "ING_Name")
			if userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				print ("New ING added")

				newIng = ING(userName.text())
				newIng.save(database)
				#update QlistView in mainWindow
				mainWindow.update_ING_tableView(database.getContent())
		else:
			print('Nop')

