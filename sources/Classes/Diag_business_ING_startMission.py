from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_business_ING_startMission(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to start a mission for the
	selected engineer
	"""
	def __init__(self, viewPath, selectedIng, database, mainWindow):
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
			if (clientName.text() == ""):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Client Name cannot be empty')
				alert.exec_()
			if (missionStartDate.date() > missionStopDate.date()):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Stop mission happens before Start mission')
				alert.exec_()

			# add info to BD
			ingID = ING.getIngIDfromName(selectedIng, database)
			content["INGs"][ingID]["current_client"] = clientName.text()
			content["INGs"][ingID]["mission_Start"] = missionStartDate.date().toString("dd.MM.yyyy")
			content["INGs"][ingID]["mission_Stop"] = missionStopDate.date().toString("dd.MM.yyyy")
			content["INGs"][ingID]["state"] = "with Mission"
			database.write(content)
			mainWindow.populate_ing_business_MissionIO(ingID)
		else:
			print ("Nop")
