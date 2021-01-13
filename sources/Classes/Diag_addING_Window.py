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

		self.userName = self.findChild(QtWidgets.QLineEdit,			"name")
		self.userEntryDate = self.findChild(QtWidgets.QDateEdit,	"entryDate")
		self.bu = self.findChild(QtWidgets.QComboBox, 				"BU")
		self.bu.currentIndexChanged.connect(self._populate_managerList)
		self.userManager = self.findChild(QtWidgets.QComboBox,		"manager")

		# set entryDate to current Date
		self.userEntryDate.setDate(QtCore.QDate.currentDate())

		# populate Bu combobox
		if len(self.dbContent["BUs"]) == 0:
			self.bu.addItem("None")
		for buName in self.dbContent["BUs"]:
			self.bu.addItem(buName)

		# populate manager combobox
		self._populate_managerList()

		# update entry date with current day
		self.userEntryDate.setDate(QtCore.QDate().currentDate())

		self.userInputCheck = False # store condition to exit the loop in case of wrong input

		while not self.userInputCheck:
			# prompt dialog
			resp = self.exec_()
			# get user input
			self.userNameText = self.userName.text().replace(',', ' ')
			self.userManagerText = self.userManager.currentText()
			#check user input
			if resp == QtWidgets.QDialog.Accepted:
				if self.userNameText == "":
					self._sendAlert("error - Name cannot be empty")
					continue
				if self.userNameText != "":
					# check if name already exists
					if self.userNameText in ING.getNames(self.database):
						self._sendAlert("error - UserName already exist")
						continue
					else:
						self.userInputCheck = True
						self._addIng()
			# case cancel
			else:
				break

	def _populate_managerList(self):
		IAsNamelist = []
		self.userManager.clear()
		for ia in self.dbContent["IAs"]:
			if self.bu.currentText() in self.dbContent["IAs"][ia]["BU"]:
				IAsNamelist.append(self.dbContent["IAs"][ia]["name"])
		if IAsNamelist == []:
				IAsNamelist.append("None")
		self.userManager.addItems(IAsNamelist)

	def _sendAlert(self, message):
		alert = QtWidgets.QMessageBox()
		alert.setText(message)
		alert.exec_()

	def _addIng(self):
		#add new ING to db
		newIng = ING(self.userNameText, self.database)
		newIng.setEntryDate(self.userEntryDate.date().toString("dd.MM.yyyy"))
		# if ING as manager => add ing in InChargeOF (IA)
		if self.userManagerText != "None":
			manager = IngAffaire.load(self.database, self.userManagerText)
			manager.putInChargeOf(self.userNameText, newIng.getType())
			manager.save()
			newIng.setManagerID(manager.getID())
			newIng.setManagerName(self.userManagerText)
		else:
			newIng.setManagerName(None)
		newIng.setState(ING.ING_STATE_IC)
		newIng.setBu(self.bu.currentText())
		newIng.save()