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
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedIng)

		missionStartDate = self.findChild(QtWidgets.QDateEdit, "startDate")
		missionStopDate = self.findChild(QtWidgets.QDateEdit, "stopDate")
		clientName = self.findChild(QtWidgets.QLineEdit, "clientName")

		missionStartDate.setDate(QtCore.QDate.currentDate())
		missionStopDate.setDate(QtCore.QDate.currentDate().addMonths(3))

		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			ing = ING.load(database, selectedIng)
			#check user input
			clientNameText = clientName.text()
			clientNameCheck = False
			dateCheck = False
			isArchived = False
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
			elif missionStopDate.date() < QtCore.QDate.currentDate():
				alert = QtWidgets.QMessageBox()
				alert.setText('Warning - Mission stop already passed -\nMission registered has archived\n{name} state stays {state}'.format(name=selectedIng, state=ing.getState()))
				alert.exec()
				isArchived = True
				prevState = ing.getStateKey()
			else:
				dateCheck = True

			# add info to BD
			if clientNameCheck and (dateCheck or isArchived):
				ing.setCurrentClient(clientNameText)
				ing.setMissionStart(missionStartDate.date().toString("dd.MM.yyyy"))
				ing.setMissionStop(missionStopDate.date().toString("dd.MM.yyyy"))
				ing.setState(ING.ING_STATE_MI)
				ing.save()
				if (isArchived):
					ing.stopMission(prevState)
					ing.save()
		else:
			print ("Nop")
