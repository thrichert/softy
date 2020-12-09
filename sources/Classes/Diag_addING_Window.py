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
		self.dbContent = database.getContent()

		self.userName = self.findChild(QtWidgets.QLineEdit,			"ING_Name")
		self.userEntryDate = self.findChild(QtWidgets.QDateEdit,	"ING_entryDate")
		self.userManager = self.findChild(QtWidgets.QComboBox,		"ING_managerComboList")
		self.userState = self.findChild(QtWidgets.QComboBox,		"ING_stateComboList")
		self.userClient = self.findChild(QtWidgets.QLineEdit,		"ING_Client")
		self.bu = self.findChild(QtWidgets.QComboBox, 				"ING_BUComboList")
		self.bu.currentIndexChanged.connect(self._populate_managerList)

		# populate Bu combolist
		for buName in self.dbContent["BUs"]:
			self.bu.addItem(buName)

		# update entry date with current day
		self.userEntryDate.setDate(QtCore.QDate().currentDate())


		# populate ING_managerComboList
		#self._populate_managerList()

		userInputsCheck = False # store condition to exit the loop in case of wrong input

		while not userInputsCheck:
			# get user input
			resp = self.exec_()
			self.userNameText = self.userName.text()
			self.userclientText = self.userClient.text()
			self.userStateText = self.userState.currentText()
			#check user input
			if resp == QtWidgets.QDialog.Accepted:
				if self.userNameText == "":
					self._sendAlert("error - Name cannot be empty")
					continue
				if self.userStateText == "With Mission" and self.userclientText == "":
					self._sendAlert("error - Client's Name cannot be empty if " + self.userNameText + " is in a mission")
					continue
				if self.userNameText != "":
					# check if name already exists
					names = []
					for ing in self.dbContent["INGs"]:
						names.append(self.dbContent["INGs"][ing]["name"])
					if self.userNameText in names:
						self._sendAlert("error - UserName already exist")
						continue
					else:
						userInputsCheck = True
						self._addIng()
			# case cancel
			else:
				break





	def _populate_managerList(self):
		IAsNamelist = ["None"]
		self.userManager.clear()
		for ia in self.dbContent["IAs"]:
			if self.dbContent["IAs"][ia]["BU"] == self.bu.currentText():
				IAsNamelist.append(self.dbContent["IAs"][ia]["name"])
		self.userManager.addItems(IAsNamelist)

	def _sendAlert(self, message):
		alert = QtWidgets.QMessageBox()
		alert.setText(message)
		alert.exec_()

	def _addIng(self):
		#add new ING to db
		#get max key from current and archive ID

		newIng = ING(self.userNameText, self.database)
		newIng.setEntryDate(self.userEntryDate.date().toString("dd.MM.yyyy"))

		# if ING as manager => add ing in InChargeOF (IA)
		if self.userManager.currentText() != "None":
			ia_id = IngAffaire.getIngAffaireIDfromName(self.userManager.currentText(), self.database)
			#TO DO : add IngAffaire Method to update IA inChargeOf field
			self.dbContent["IAs"][ia_id]["inChargeOf"]["INGs"].append(self.userNameText)
			newIng.setManagerID(ia_id)
			newIng.setManagerName(self.userManager.currentText())
		self.database.write(self.dbContent)
		newIng.setCurrentClient(self.userClient.text())
		newIng.setState(self.userStateText)
		newIng.setBu(self.bu.currentText())
		newIng.save(self.database)