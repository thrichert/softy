from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.ING import ING
from Classes.IngAffaire import IngAffaire

class Diag_addING_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create an Engineer
	"""
	def __init__(self, viewPath, database):
		super(Diag_addING_Window, self).__init__()
		uic.loadUi(viewPath,self)
		content = database.getContent()

		userName = self.findChild(QtWidgets.QLineEdit,		"ING_Name")
		userEntryDate = self.findChild(QtWidgets.QDateEdit,	"ING_entryDate")
		userManager = self.findChild(QtWidgets.QComboBox,	"ING_managerComboList")
		userState = self.findChild(QtWidgets.QComboBox,		"ING_stateComboList")
		userClient = self.findChild(QtWidgets.QLineEdit,	"ING_Client")

		# populate ING_managerComboList
		IAsIDlist = content["IAs"].keys()
		IAsNamelist = []
		for ia in IAsIDlist:
			IAsNamelist.append(content["IAs"][ia]["name"])
		userManager.addItems(IAsNamelist)

		# autofill QDateEdit with today's date
		userEntryDate.setDate(QtCore.QDate().currentDate())

		resp = self.exec_()

		#check user input
		userNameCheck = False
		userNameText = userName.text()
		if resp == QtWidgets.QDialog.Accepted:
			if userNameText == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			if userNameText != "":
				# check if name already exists
				names = []
				for ing in content["INGs"]:
					names.append(content["INGs"][ing]["name"])
				if userNameText in names:
					alert = QtWidgets.QMessageBox()
					alert.setText("error - UserName already exist")
					alert.exec_()
				else:
					userNameCheck = True

			if userNameCheck:
				#add new ING to db
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

				newIng = ING(userNameText, NbrIng)
				newIng.setEntryDate(userEntryDate.date().toString("dd.MM.yyyy"))

				# if ING as manager => add ing in InChargeOF (IA)
				if userManager.currentText() != "None":
					ia_id = IngAffaire.getIngAffaireIDfromName(userManager.currentText(), database)
					content["IAs"][ia_id]["inChargeOf"].append(userName.text())
					newIng.setManager(ia_id)
				database.write(content)
				newIng.setCurrentClient(userClient.text())
				newIng.setState(userState.currentText())
				newIng.save(database)

		else:
			print('Nop')

