from PyQt5 import QtWidgets, uic, QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_business_ING_startMission(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to start a mission for the
	selected engineer
	"""
	def __init__(self, viewPath, selectedIng, database):
		super(Diag_business_ING_startMission, self).__init__()
		uic.loadUi(viewPath, self)
		content = database.getContent()
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedIng)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			missionStartDate = self.findChild(QtWidgets.QDateEdit, "startDate")
			missionStopDate = self.findChild(QtWidgets.QDateEdit, "stopDate")
			clientName = self.findChild(QtWidgets.QLineEdit, "clientName")
			#check user input
			clientNameText = clientName.text()
			clientNameCheck = False
			dateCheck = False
			if (clientNameText == ""):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Client Name cannot be empty')
				alert.exec_()
			else:
				clientNameCheck = True
			if (missionStartDate.date() > missionStopDate.date()):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Stop mission happens before Start mission')
				alert.exec_()
			else:
				dateCheck = True

			# add info to BD
			if clientNameCheck and dateCheck:
				ingID = ING.getIngIDfromName(selectedIng, database)
				content["INGs"][ingID]["current_client"] = clientNameText
				content["INGs"][ingID]["mission_Start"] = missionStartDate.date().toString("dd.MM.yyyy")
				content["INGs"][ingID]["mission_Stop"] = missionStopDate.date().toString("dd.MM.yyyy")
				content["INGs"][ingID]["state"] = "with Mission"
				database.write(content)
		else:
			print ("Nop")
