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
		self.database = database
		content = database.getContent()

		self.userName = self.findChild(QtWidgets.QLineEdit,			"ING_Name")
		self.userEntryDate = self.findChild(QtWidgets.QDateEdit,	"ING_entryDate")
		self.userManager = self.findChild(QtWidgets.QComboBox,		"ING_managerComboList")
		self.userState = self.findChild(QtWidgets.QComboBox,		"ING_stateComboList")
		self.userClient = self.findChild(QtWidgets.QLineEdit,		"ING_Client")
		self.bu = self.findChild(QtWidgets.QComboBox, 				"ING_BUComboList")
		self.bu.currentIndexChanged.connect(self._populate_managerList)

		# populate Bu combolist
		for buName in content["BUs"]:
			self.bu.addItem(buName)

		# populate ING_managerComboList
		#self._populate_managerList()



		# autofill QDateEdit with today's date
		self.userEntryDate.setDate(QtCore.QDate().currentDate())

		resp = self.exec_()

		#check user input
		userNameCheck = False
		userNameText = self.userName.text()
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
				newIng.setEntryDate(self.userEntryDate.date().toString("dd.MM.yyyy"))

				# if ING as manager => add ing in InChargeOF (IA)
				if self.userManager.currentText() != "None":
					ia_id = IngAffaire.getIngAffaireIDfromName(self.userManager.currentText(), database)
					content["IAs"][ia_id]["inChargeOf"]["INGs"].append(self.userName.text())
					newIng.setManagerID(ia_id)
					newIng.setManagerName(self.userManager.currentText())
				database.write(content)
				newIng.setCurrentClient(self.userClient.text())
				newIng.setState(self.userState.currentText())
				newIng.setBu(self.bu.currentText())
				newIng.save(database)

		else:
			print('Nop')


	def _populate_managerList(self):
		content = self.database.getContent()
		IAsNamelist = ["None"]
		self.userManager.clear()
		for ia in content["IAs"]:
			if content["IAs"][ia]["BU"] == self.bu.currentText():
				IAsNamelist.append(content["IAs"][ia]["name"])
		self.userManager.addItems(IAsNamelist)
