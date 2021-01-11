from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.ING import ING
from Classes.IngAffaire import IngAffaire
from Classes.User import User


class Diag_delete_ing_ia(QtWidgets.QDialog):
	"""
	Class that handle a dialog window to delete an Engineer or an BusinessIng
	"""

	def __init__(self, viewPath, userType, selectedUsr, database):
		super(Diag_delete_ing_ia, self).__init__()
		uic.loadUi(viewPath, self)
		self.deleted = False

		# modify group box name
		self.groupboxName = self.findChild(QtWidgets.QGroupBox, "Ing_groupBox")
		self.groupboxName.setTitle(selectedUsr)

		self.endContractDateEdit = self.findChild(QtWidgets.QDateEdit,	"contract_end_date")
		self.endContractDateEdit.setDate(QtCore.QDate.currentDate())

		self.motifEndContract = self.findChild(QtWidgets.QLineEdit,		"motif")

		resp = self.exec_()

		if resp == QtWidgets.QDialog.Accepted:
			if userType == User._ING:
				usr = ING.load(database, selectedUsr)
			elif userType == User._IA:
				usr = IngAffaire.load(database, selectedUsr)
			else:
				usr = None
				print ("error - {} not found".format(selectedUsr))
				return
			ingEntryDate = usr.getEntryDate()

			self.motifText = self.motifEndContract.text()
			self.exitDateText = self.endContractDateEdit.date().toString('dd.MM.yyyy')
			motifCheck = False
			dateCheck = False
			#check user Input
			if self.motifText == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - Motif cannot be empty")
				alert.exec_()
			else:
				motifCheck = True
			if self.endContractDateEdit.date() < QtCore.QDate.fromString(ingEntryDate,'dd.MM.yyyy') :
				alert = QtWidgets.QMessageBox()
				alert.setText('error - end contract happens before entry date')
				alert.exec_()
			else:
				dateCheck = True
			self.deleted = (dateCheck and motifCheck)
			if self.deleted:
				usr.delete(self.exitDateText, self.motifText)
