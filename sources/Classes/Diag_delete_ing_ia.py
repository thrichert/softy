from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.ING import ING


class Diag_delete_ing_ia(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to delete an Engineer or an BusinessIng
	"""

	def __init__(self, viewPath, selectedIng, database):
		super(Diag_delete_ing_ia, self).__init__()
		uic.loadUi(viewPath, self)
		content = database.getContent()
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedIng)

		self.endContractDateEdit = self.findChild(QtWidgets.QDateEdit,	"contract_end_date")
		self.endContractDateEdit.setDate(QtCore.QDate.currentDate())

		self.motifEndContract = self.findChild(QtWidgets.QLineEdit,		"motif")

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:

			ingID = ING.getIngIDfromName(selectedIng, database)
			ingEntryDate = QtCore.QDate().fromString(content["INGs"][ingID]['entryDate'], 'dd.MM.yyyy')

			motifCheck = False
			dateCheck = False
			#check user Input
			if self.motifEndContract.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - Motif cannot be empty")
				alert.exec_()
			else:
				motifCheck = True
			if self.endContractDateEdit.date() < ingEntryDate:
				alert = QtWidgets.QMessageBox()
				alert.setText('error - end contract happens before entry date')
				alert.exec_()
			else:
				dateCheck = True

			if dateCheck and motifCheck:
				ingData = content["INGs"][ingID]
				# remove ing from Ings
				content["INGs"].pop(ingID)
				# add data to Archives
				content["archive"]["INGs"][ingID] = ingData
				content["archive"]["INGs"][ingID]["endContract"] = self.endContractDateEdit.date().toString('dd.MM.yyyy')
				content["archive"]["INGs"][ingID]["motif"] = self.motifEndContract.text()

				#save db
				database.write(content)
