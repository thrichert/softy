from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING
from Classes.User import User

class Diag_addIA_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Business Engineer
	"""
	def __init__(self, viewPath, database):
		super(Diag_addIA_Window, self).__init__()
		uic.loadUi(viewPath,self)
		self.database = database
		self.dbContent = database.getContent()
		self.added = False
		self.buText = ''
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
		for i, bu in self.dbContent["BUs"].items():
			self.bu.addItem(i)


		INGs = self.dbContent["INGs"]
		i = 0
		for ing in INGs:
			if INGs[ing]["manager"] == None:
				self.INGs_checkBox.append(QtWidgets.QCheckBox(INGs[ing]["name"]))
				self.scrollAreaLayout_INGs.addWidget(self.INGs_checkBox[i])
				i += 1

		self._on_userRole_changed()

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
		self.userManager.clear()
		self.dbContent = self.database.getContent()
		if self.buText != '':
			IAs = self.dbContent["BUs"][self.buText]
		else:
			IAs = self.dbContent["IAs"]

		#if self.userRole.currentText() != IngAffaire.ROLES[IngAffaire._IA_ROLE_IA]:
		self.IAs_checkBox = []
		i = 0
		for ia in IAs:
			if IAs[ia]["manager"] == None and self.userRole.currentIndex() > int(IAs[ia]["role"]):
				self.IAs_checkBox.append(QtWidgets.QCheckBox(IAs[ia]["name"]))
				self.scrollAreaLayout_IAs.addWidget(self.IAs_checkBox[i])
				i += 1
			if IAs[ia]["role"] > self.userRole.currentIndex():
				self.userManager.addItem(IAs[ia]["name"])

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
		self.added = True
		self.newIA = IngAffaire(self.userNameText, self.database)
		self.newIA.setEntryDate(self.userEntryDateText)
		if self.ManagerText != "":
			manager = IngAffaire.load(self.database, self.ManagerText)
			manager.putInChargeOf(self.userNameText, self.newIA.getType())
			manager.save()
			self.newIA.setManagerID(manager.getID())
			self.newIA.setManagerName(self.ManagerText)
		else:
			self.newIA.setManagerName(None)
		for roleId, roletxt in IngAffaire.ROLES.items():
			if roletxt == self.userRoleText:
				self.newIA.setRole(roleId)

		for ia in self.IAs_checkBox:
			if ia.isChecked():
				managedIa =  IngAffaire.load(self.database, ia.text())
				managedIa.setManagerName(self.userNameText)
				managedIa.setManagerID(self.newIA.getID())
				managedIa.setBu(self.buText)
				managedIa.save()
				self.newIA.putInChargeOf(ia.text(), "IAs")
		# update other ING whose are now managed by this new IA
		for ing in self.INGs_checkBox:
			if ing.isChecked():
				managedIng = ING.load(self.database, ing.text())
				managedIng.setManagerName(self.userNameText)
				managedIng.setManagerID(self.newIA.getID())
				managedIng.setBu(self.buText)
				managedIng.save()
				self.newIA.putInChargeOf(ing.text(), "INGs")
		self.newIA.setBu(self.buText)
		self.newIA.save()