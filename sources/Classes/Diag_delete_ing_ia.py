from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.ING import ING


class Diag_delete_ing_ia(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to delete an Engineer or an BusinessIng
	"""

	def __init__(self, viewPath, selectedIng, database, mainWindow):
		super(Diag_delete_ing_ia, self).__init__()
		uic.loadUi(viewPath, self)
		content = database.getContent()
		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedIng)

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:
			endContractDateEdit = self.findChild(QtWidgets.QDateEdit, "contract_end_date")
			motifEndContract = self.findChild(QtWidgets.QLineEdit, "motif")
			ingID = ING.getIngIDfromName(selectedIng, database)

			ingEntryDate = QtCore.QDate().fromString(content["INGs"][ingID]['entryDate'], 'dd.MM.yyyy')


			motifCheck = False
			dateCheck = False
			#check user Input
			if motifEndContract.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - Motif cannot be empty")
				alert.exec_()
			else:
				motifCheck = True
			if endContractDateEdit.date() < ingEntryDate:
				alert = QtWidgets.QMessageBox()
				alert.setText('error - end contract happens before entry date')
				alert.exec_()
			else:
				dateCheck = True

			if dateCheck and motifCheck:
				print ("DA")
				# Update Database
				# get previous data
				ingData = content["INGs"][ingID]
				# remove ing from Ings
				content["INGs"].pop(ingID)
				# add data to Archives
				content["archive"]["INGs"][ingID] = ingData
				content["archive"]["INGs"][ingID]["endContract"] = endContractDateEdit.date().toString('dd.MM.yyyy')
				content["archive"]["INGs"][ingID]["motif"] = motifEndContract.text()

				#save db
				database.write(content)

				# update Views
				mainWindow.update_ING_tableView(database.getContent())
				mainWindow.update_business_ING_listView(database.getContent())
