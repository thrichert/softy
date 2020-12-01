from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_business_ING_stopMission(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to stop a mission for the
	selected engineer
	"""
	def __init__(self, viewPath, selectedIng, database):
		super(Diag_business_ING_stopMission, self).__init__()
		uic.loadUi(viewPath, self)

		content = database.getContent()
		ingID = ING.getIngIDfromName(selectedIng, database)
		ingData = content["INGs"][ingID]


		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox,		"Ing_groupBox")
		self.groupboxName.setTitle(ingData["name"])

		# auto fill data if available
		self.ingState = self.findChild(QtWidgets.QComboBox,			"ing_State_comboBox")
		self.currentClient = self.findChild(QtWidgets.QLineEdit,	"currentClient")
		self.missionStopDate = self.findChild(QtWidgets.QDateEdit,	"stopDate")

		self.ingState.setCurrentText(ingData["state"])
		self.missionStopDate.setDate(QtCore.QDate().fromString(ingData["mission_Stop"], "dd.MM.yyyy"))
		self.currentClient.setText(ingData["current_client"])

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:
			ingID = ING.getIngIDfromName(selectedIng, database)
			missionStartDate = QtCore.QDate().fromString(content["INGs"][ingID]["mission_Start"],"dd.MM.yyyy")
			#check user input
			dateCheck = False
			if (self.missionStopDate.date() < missionStartDate):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Stop mission happens before Start mission')
				alert.exec_()
			else:
				dateCheck = True
			# add info to BD
			if dateCheck:
				content["INGs"][ingID]["current_client"] = ""
				content["INGs"][ingID]["mission_Stop"] = self.missionStopDate.date().toString("dd.MM.yyyy")
				content["INGs"][ingID]["state"] = self.ingState.currentText()
				database.write(content)

		else:
			print ("Nop")
