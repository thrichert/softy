from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_addBU_Window(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to create a Business Unit [BU]
	"""
	def __init__(self, viewPath, database):
		super(Diag_addBU_Window, self).__init__()
		uic.loadUi(viewPath,self)
		content = database.getContent()
		# load elements

		self.BU_name_lineEdit = self.findChild(QtWidgets.QLineEdit, "BU_name")
		self.scrollAera_IAs = self.findChild(QtWidgets.QScrollArea, "scrollArea_IAs")
		self.scrollAera_INGs = self.findChild(QtWidgets.QScrollArea, "scrollArea_INGs")
		self.containerWidget_IAs = QtWidgets.QWidget()
		self.containerWidget_INGs = QtWidgets.QWidget()

		self.scrollAreaLayout_IAs = QtWidgets.QVBoxLayout()
		self.scrollAreaLayout_INGs = QtWidgets.QVBoxLayout()

		self.containerWidget_IAs.setLayout(self.scrollAreaLayout_IAs)
		self.containerWidget_INGs.setLayout(self.scrollAreaLayout_INGs)

		# populate IAs & INGs scroll area
		IAs = content["IAs"]
		INGs = content["INGs"]

		self.IAs_checkBox = []
		self.INGs_checkBox = []
		for i, ia in enumerate(IAs):
			self.IAs_checkBox.append(QtWidgets.QCheckBox(IAs[ia]["name"]))
			self.scrollAreaLayout_IAs.addWidget(self.IAs_checkBox[i])

		for i, ing in enumerate(INGs):
			self.INGs_checkBox.append(QtWidgets.QCheckBox(INGs[ing]["name"]))
			self.scrollAreaLayout_INGs.addWidget(self.INGs_checkBox[i])

		self.scrollAera_INGs.setWidget(self.containerWidget_INGs)
		self.scrollAera_IAs.setWidget(self.containerWidget_IAs)

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:


			BuName_text = self.BU_name_lineEdit.text()

			BuNameslist = content["BUs"].keys()

			BuNameCheck = False
			#check if empty
			if BuName_text == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - Bu's name cannot be empty")
				alert.exec_()
			# check if already exist
			elif BuName_text in BuNameslist:
				alert = QtWidgets.QMessageBox()
				alert.setText("error - Bu : "+ BuName_text + "already exist")
				alert.exec_()
			else:
				BuNameCheck = True

			if BuNameCheck:
				BuData = {
					"IAs":[],
					"INGs":[]
				}
				for i in range(len(self.IAs_checkBox)):
					if self.IAs_checkBox[i].isChecked():
						BuData["IAs"].append(self.IAs_checkBox[i].text())
				for i in range(len(self.INGs_checkBox)):
					if self.INGs_checkBox[i].isChecked():
						BuData["INGs"].append(self.INGs_checkBox[i].text())

				content["BUs"][BuName_text] = BuData
				database.write(content)