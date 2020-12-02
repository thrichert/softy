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
		content = database.getContent()

		# get Element

		self.userName = self.findChild(QtWidgets.QLineEdit, "IA_Name")
		self.userRole = self.findChild(QtWidgets.QComboBox, "IA_Role")

		self.userRole.currentIndexChanged.connect(self._on_userRole_changed)

		self.BuSelector = self.findChild(QtWidgets.QComboBox, "BU_comboBox")
		self.ManagerSelector = self.findChild(QtWidgets.QComboBox, "Manager_comboBox")

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

		# populate IAs & INGs scroll area

		self.IAs_checkBox = []
		self.INGs_checkBox = []

		# setup elements
		for i, bu in enumerate(content["BUs"]):
			self.BuSelector.insertItem(i, bu)

		INGs = content["INGs"]
		i = 0
		for ing in INGs:
			if INGs[ing]["manager"] == None:
				self.INGs_checkBox.append(QtWidgets.QCheckBox(INGs[ing]["name"]))
				self.scrollAreaLayout_INGs.addWidget(self.INGs_checkBox[i])
				i += 1

		IAs = content["IAs"]
		for i,ia in enumerate(IAs):
			if IAs[ia]["role"] != "IA":
				self.ManagerSelector.insertItem(i, IAs[ia]["name"])
		# run
		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:
			#check user input

			if self.userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				if len(content["IAs"].keys()) == 0:
					NbrIA = 0
				else:
					NbrIA = int(max(content["IAs"].keys())) + 1

				newUser = IngAffaire(name=self.userName.text(), role=self.userRole.currentText(), bu=self.BuSelector.currentText(), manager=self.ManagerSelector.currentText(), idx=NbrIA)
				newUser.save(database)
				# update BU
				content["BUs"][self.BuSelector.currentText()]["IAs"].append(self.userName.text())
				# update Manager
				if self.ManagerSelector.currentText() != "None":
					managerID = IngAffaire.getIngAffaireIDfromName(self.ManagerSelector.currentText(), database)
					content["IAs"][managerID]["inChargeOf"]["IAs"].append(self.userName.text())
				# update other IA whose are now managed by this new IA
				for ia in self.IAs_checkBox:
					if ia.isChecked():
						iaName = ia.text()
						iaID = IngAffaire.getIngAffaireIDfromName(iaName, self.database)
						content["IAs"][iaID]["manager"] = self.userName.text()
				# update other ING whose are now managed by this new IA
				for ing in self.INGs_checkBox:
					if ing.isChecked():
						ingName = ing.text()
						ingID = ING.getIngIDfromName(ingName, self.database)
						content["INGs"][ingID]["managerID"] = NbrIA
						content["INGs"][ingID]["manager"] = self.userName.text()
				database.write(content)
		else:
			print('Nop')

	def _on_userRole_changed(self):

		self._clearLayout(self.scrollAreaLayout_IAs)

		content = self.database.getContent()
		IAs = content["IAs"]

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
