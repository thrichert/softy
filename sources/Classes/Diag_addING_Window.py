from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

class Diag_addING_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create an Engineer
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
				#get max key from current and archive ID
				ING_key = content["INGs"].keys()
				archiveING_id = content["archive"]["INGs"].keys()

				if len(ING_key) != 0 and len(archiveING_id) != 0:
					NbrIng = int(max( max(ING_key), max(archiveING_id))) + 1
				elif len(ING_key) == 0 and len(archiveING_id) != 0:
					NbrIng = int(max('0', max(archiveING_id))) + 1
				elif len(archiveING_id) == 0 and len(ING_key) != 0:
					NbrIng = int(max(max(ING_key), '0')) + 1
				else:
					NbrIng = 0

				newIng = ING(userName.text(), NbrIng)
				newIng.setEntryDate(userEntryDate.date().toString("dd.MM.yyyy"))
				#update QlistView in mainWindow
				#mainWindow.update_ING_tableView(database.getContent())

				# if ING as manager => add ing in InChargeOF (IA)
				if userManager.currentText() != "None":
					ia_id = IngAffaire.getIngAffaireIDfromName(userManager.currentText(), database)
					content["IAs"][ia_id]["inChargeOf"].append(userName.text())
					newIng.setManager(ia_id)
				newIng.setCurrentClient(userClient.text())
				newIng.setState(userState.currentText())
				newIng.save(database)
				content = database.getContent()
				mainWindow.update_ING_tableView(content)
				mainWindow.update_business_ING_listView(content)
				database.write(content)
				mainWindow.populate_ing_business_ingIO(NbrIng)
		else:
			print('Nop')

