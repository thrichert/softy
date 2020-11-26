from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

class Diag_addING_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Engineer
	"""
	def __init__(self, viewPath, database, mainWindow):
		super(Diag_addING_Window, self).__init__()
		uic.loadUi(viewPath,self)
		content = database.getContent()

		userName = self.findChild(QtWidgets.QLineEdit, "ING_Name")
		userEntryDate = self.findChild(QtWidgets.QDateEdit, "ING_entryDate")
		userManager = self.findChild(QtWidgets.QComboBox, "ING_managerComboList")
		userState = self.findChild(QtWidgets.QComboBox, "ING_stateComboList")
		userClient = self.findChild(QtWidgets.QLineEdit, "ING_Client")

		# populate ING_managerComboList
		IAsIDlist = content["IAs"].keys()
		IAsNamelist = []
		for ia in IAsIDlist:
			IAsNamelist.append(content["IAs"][ia]["name"])
		userManager.addItems(IAsNamelist)

		resp = self.exec_()
		#check user input
		if resp == QtWidgets.QDialog.Accepted:
			if userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				if len(content["INGs"].keys()) == 0:
					NbrIng = 0
				else:
					NbrIng = int(max(content["INGs"].keys())) + 1
				newIng = ING(userName.text(), NbrIng)
				newIng.setEntryDate(userEntryDate.date().toString("MM.yyyy"))
				#update QlistView in mainWindow
				mainWindow.update_ING_tableView(database.getContent())
				mainWindow.update_business_ING_listView(database.getContent())
				# if ING as manager => add ing in InChargeOF (IA)
				if userManager.currentText() != "None":
					ia_id = IngAffaire.getIngAffaireIDfromName(userManager.currentText(), database)
					content["IAs"][ia_id]["inChargeOf"].append(userName.text())
					newIng.setManager(ia_id)
				newIng.setCurrentClient(userClient.text())
				newIng.setState(userState.currentText())
				newIng.save(database)
				database.write(content)
		else:
			print('Nop')

