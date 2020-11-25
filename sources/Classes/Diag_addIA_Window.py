from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_addIA_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Business Engineer
	"""
	def __init__(self, viewPath, database, mainWindow):
		super(Diag_addIA_Window, self).__init__()
		uic.loadUi(viewPath,self)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			#check user input
			userName = self.findChild(QtWidgets.QLineEdit, "IA_Name")
			userRole = self.findChild(QtWidgets.QComboBox, "IA_Role")
			if userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				print ("New IA added")

				newUser = IngAffaire(userName.text(), userRole.currentText())
				newUser.save(database)
				#update QlistView in mainWindow
				mainWindow.update_IA_tableView(database.getContent())
		else:
			print('Nop')
