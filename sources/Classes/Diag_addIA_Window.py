from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_addIA_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Business Engineer
	"""
	def __init__(self, viewPath, database):
		super(Diag_addIA_Window, self).__init__()
		uic.loadUi(viewPath,self)
		self.database = database
		self.dbContent = database.getContent()

		# get Element

		self.userName = self.findChild(QtWidgets.QLineEdit,			"name")
		self.userEntryDate = self.findChild(QtWidgets.QDateEdit,	"entryDate")
		self.bu = self.findChild(QtWidgets.QComboBox,				"BU")
		self.userRole = self.findChild(QtWidgets.QComboBox,			"role")
		self.userRole.currentIndexChanged.connect(self._on_userRole_changed)
		self.userManager = self.findChild(QtWidgets.QComboBox,		"manager")

		self.scrollAera_IAs = self.findChild(QtWidgets.QScrollArea, "scrollArea_IAs")
		self.scrollAera_INGs = self.findChild(QtWidgets.QScrollArea, "scrollArea_INGs")

		self.scrollAreaLayout_IAs = QtWidgets.QVBoxLayout()
		self.scrollAreaLayout_INGs = QtWidgets.QVBoxLayout()
		self.containerIAs = QtWidgets.QWidget()
		self.containerINGs = QtWidgets.QWidget()

		self.containerIAs.setLayout(self.scrollAreaLayout_IAs)
		self.containerINGs.setLayout(self.scrollAreaLayout_INGs)

		self.scrollArea_IAs.setWidget(self.containerIAs)
		self.scrollArea_INGs.setWidget(self.containerINGs)

		# set entryDate to current Date
		self.userEntryDate.setDate(QtCore.QDate.currentDate())

		for role in IngAffaire.ROLES:
			self.userRole.addItem(IngAffaire.ROLES[role])

		# populate IAs & INGs scroll area
		self.IAs_checkBox = []
		self.INGs_checkBox = []
		# setup elements
		for buName in self.dbContent["BUs"]:
			self.bu.addItem(buName)

		INGs = self.dbContent["INGs"]
		i = 0
		for ing in INGs:
			if INGs[ing]["manager"] == None:
				self.INGs_checkBox.append(QtWidgets.QCheckBox(INGs[ing]["name"]))
				self.scrollAreaLayout_INGs.addWidget(self.INGs_checkBox[i])
				i += 1

		IAs = self.dbContent["IAs"]
		for ia in IAs:
			if IAs[ia]["role"] != "IA":
				self.userManager.addItem(IAs[ia]["name"])
		userInputsCheck = False # store condition to exit the loop in case of wrong input

		while not userInputsCheck:
			# run
			resp = self.exec_()
			# get user input
			self.userNameText = self.userName.text()
			self.userRoleText = self.userRole.currentText()
			self.ManagerText = self.userManager.currentText()
			self.buText = self.bu.currentText()
			self.userEntryDateText = self.userEntryDate.date().toString("dd.MM.yyyy")
			if resp == QtWidgets.QDialog.Accepted:
				#check user input
				if self.userNameText == "":
					self._sendAlert("error - UserName cannot be empty")
					continue
				if self.userNameText != "":
					if self.userNameText in IngAffaire.getNames(self.database):
						self._sendAlert("error - UserName already exist")
						continue
					else:
						userInputsCheck = True
						self._addIA()
						# update BU
						self.dbContent["BUs"][self.buText]["IAs"].append(self.userNameText)
						# update Manager
						if self.ManagerText != "None":
							managerID = IngAffaire.getIngAffaireIDfromName(self.ManagerText, database)
							self.dbContent["IAs"][managerID]["inChargeOf"]["IAs"].append(self.userNameText)
						# update other IA whose are now managed by this new IA
						for ia in self.IAs_checkBox:
							if ia.isChecked():
								iaName = ia.text()
								iaID = IngAffaire.getIngAffaireIDfromName(iaName, self.database)
								self.dbContent["IAs"][iaID]["manager"] = self.userNameText
						# update other ING whose are now managed by this new IA
						for ing in self.INGs_checkBox:
							if ing.isChecked():
								ingName = ing.text()
								ingID = ING.getIngIDfromName(ingName, self.database)
								self.dbContent["INGs"][ingID]["managerID"] = self.newIA.getID()
								self.dbContent["INGs"][ingID]["manager"] = self.userNameText
						database.write(self.dbContent)
			# case cancel
			else:
				break


	def _sendAlert(self, message):
		alert = QtWidgets.QMessageBox()
		alert.setText(message)
		alert.exec_()

	def _on_userRole_changed(self):
		self._clearLayout(self.scrollAreaLayout_IAs)

		self.dbContent = self.database.getContent()
		IAs = self.dbContent["IAs"]

		if self.userRole.currentText() != "IA":
			self.IAs_checkBox = []
			i = 0
			for ia in IAs:
				if IAs[ia]["manager"] == "None":
					self.IAs_checkBox.append(QtWidgets.QCheckBox(IAs[ia]["name"]))
					self.scrollAreaLayout_IAs.addWidget(self.IAs_checkBox[i])
					i += 1

	def _clearLayout(self, layout):
		if layout is not None:
			while layout.count():
				item = layout.takeAt(0)
				widget = item.widget()
				if widget is not None:
					widget.deleteLater()
				else:
					self.clearLayout(item.layout())

	def _addIA(self):
		self.newIA = IngAffaire(self.userNameText, self.database)
		self.newIA.setEntryDate(self.userEntryDateText)
		self.newIA.setManagerName(self.ManagerText)
		for roleId, roletxt in IngAffaire.ROLES.items():
			if roletxt == self.ManagerText:
				self.newIA.setRole(roleId)
		self.newIA.setBu(self.buText)
		self.newIA.save()