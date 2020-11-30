from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

class Diag_business_ING_stopMission(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to stop a mission for the
	selected engineer
	"""
	def __init__(self, viewPath, selectedIng, database, mainWindow):
		super(Diag_business_ING_stopMission, self).__init__()
		uic.loadUi(viewPath, self)

		content = database.getContent()
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedIng)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			missionStopDate = self.findChild(QtWidgets.QDateEdit, "stopDate")
			ingState = self.findChild(QtWidgets.QComboBox, "ing_State_comboBox")
			ingID = ING.getIngIDfromName(selectedIng, database)
			missionStartDate = QtCore.QDate().fromString(content["INGs"][ingID]["mission_Start"],"dd.MM.yyyy")
			#check user input
			if (missionStopDate.date() > missionStartDate):
				alert = QtWidgets.QMessageBox()
				alert.setText('error - Stop mission happens before Start mission')
				alert.exec_()

			# add info to BD
			content["INGs"][ingID]["current_client"] = None
			content["INGs"][ingID]["mission_Stop"] = missionStopDate.date().toString("dd.MM.yyyy")
			content["INGs"][ingID]["state"] = ingState.currentText()
			database.write(content)
			mainWindow.populate_ing_business_MissionIO(ingID)
		else:
			print ("Nop")
