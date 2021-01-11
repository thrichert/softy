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

		ing = ING.load(database, selectedIng)
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox,		"Ing_groupBox")
		self.groupboxName.setTitle(ing.getName())

		# auto fill data if available
		self.ingState = self.findChild(QtWidgets.QComboBox,			"ing_State_comboBox")
		self.missionStopDate = self.findChild(QtWidgets.QDateEdit,	"stopDate")

		for idx, state in ING.STATES.items():
			if idx != ING.ING_STATE_MI:
				self.ingState.addItem(state)

		self.missionStopDate.setDate(QtCore.QDate().fromString(ing.getMissionStop(), "dd.MM.yyyy"))

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:
			missionStartDate = QtCore.QDate().fromString(ing.getMissionStart(), "dd.MM.yyyy")
			nextState = self.ingState.currentText()
			nextStateKey = list(ING.STATES.values()).index(nextState)
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
				#save previous missions data:
				ing.saveCurrentMission()
				ing.stopMission(int(nextStateKey), self.missionStopDate.date().toString('dd.MM.yyyy'))
				ing.save()

		else:
			print ("Nop")
