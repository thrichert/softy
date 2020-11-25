from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.Diag_addIA_Window import Diag_addIA_Window
from Classes.Diag_addING_Window import Diag_addING_Window
from Classes.IngAffaire import IngAffaire

class MainWindow(QtWidgets.QMainWindow):
	"""
	Class that handle the main window
	"""
	def __init__(self, database):
		super(MainWindow, self).__init__()
		uic.loadUi("./sources/views/mainWindow.ui", self)
		self.database = database
		#
		#	tab : ADM
		#
		# PushButton Action
		self.addNew_IA = self.findChild(QtWidgets.QPushButton, "addNewIA")
		self.addNew_IA.clicked.connect(self.on_addNew_IA)
		self.addNew_ING = self.findChild(QtWidgets.QPushButton, "addNewING")
		self.addNew_ING.clicked.connect(self.on_addNew_ING)

		# setup IAs QtableView
		self.IAs_model = QtGui.QStandardItemModel()
		self.IAs_model.setColumnCount(2)
		self.IAs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
		self.IAs_model.setHeaderData(1, QtCore.Qt.Horizontal, "Role")

		# setup INGs QtableView
		self.INGs_model = QtGui.QStandardItemModel()
		self.INGs_model.setColumnCount(1)
		self.INGs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")


		# populate user list in QtableViews
		self.update_IA_tableView(database.getContent())
		self.update_ING_tableView(database.getContent())

		#
		#	tab : activite
		#
		self.currentWeek = None
		self.selectedIA = None

		# calendar callback on day select
		self.activity_calendar = self.findChild(QtWidgets.QCalendarWidget, "activityCalendar")
		self.activity_calendar.clicked.connect(self.on_calendar_select)

		# setup IAs list
		self.update_activity_IA_list(database.getContent())
		self.activity_IAs_list.clicked.connect(self.on_activity_IAselected)

		# setup activity QtableView
		self.activity_model = QtGui.QStandardItemModel()
		self.activity_model.setColumnCount(10)
		headers = ["Prosp", "Nvx Besoin","Besoins Actifs", "KLIF", "START", "Push DC", "EC1", "EC2", "PPLES", "RH+"]
		for i, h in enumerate(headers):
			self.activity_model.setHeaderData(i, QtCore.Qt.Horizontal, h)
		self.activity_model.insertRow(0)
		self.activity_model.dataChanged.connect(self.on_activity_table_dataChange)

		# display window
		self.show()

	def on_addNew_IA(self):
		self.add_IA_Diag = Diag_addIA_Window("./sources/views/add_IA_Diag.ui", self.database, self)

	def on_addNew_ING(self):
		self.add_ING_Diag = Diag_addING_Window("./sources/views/add_ING_Diag.ui", self.database, self)

	def update_IA_tableView(self, data):
		# get info from DB
		self.IAs_list = self.findChild(QtWidgets.QTableView, "IAsList")
		self.IAs_list.setModel(self.IAs_model)
		for colID, IA in enumerate(data["IAs"]):
			name = QtGui.QStandardItem(data["IAs"][IA]["name"])
			role = QtGui.QStandardItem(data["IAs"][IA]["role"])
			name.setFlags(QtCore.Qt.NoItemFlags)
			role.setFlags(QtCore.Qt.NoItemFlags)
			self.IAs_model.setItem(colID, 0, name)
			self.IAs_model.setItem(colID, 1, role)
		self.update_activity_IA_list(data)

	def update_ING_tableView(self, data):
		# get info from DB
		self.INGs_list = self.findChild(QtWidgets.QTableView, "INGsList")
		self.INGs_list.setModel(self.INGs_model)
		for colID, ING in enumerate(data["INGs"]):
			name = QtGui.QStandardItem(data["INGs"][ING]["name"])
			name.setFlags(QtCore.Qt.NoItemFlags)
			self.INGs_model.setItem(colID, 0, name)

	def update_activity_tableView(self, data, IA_name, week_year):
		self.activity_list = self.findChild(QtWidgets.QTableView, "activityList")

		# get IA's ID from his name
		ia_ID = IngAffaire.getIngAffaireIDfromName(self.selectedIA, self.database)
		print("ia_ID @ update_activity_tableView", ia_ID)

		ia_data = IngAffaire.getIngAffaireFromID(ia_ID, self.database)
		ia = IngAffaire(ia_data["name"], ia_data["role"], ia_ID)

		activities = ia.getActivitiesFromWeek(self.database, str(self.currentWeek[0])+"_"+str(self.currentWeek[1]))

		for i in range(self.activity_model.columnCount()):
			self.activity_model.setItem(0, i, QtGui.QStandardItem(str(activities[i])))
		self.activity_list.setModel(self.activity_model)

	def on_activity_IAselected(self):
		self.selectedIA = self.activity_IAs_list.currentIndex().data()
		if self.currentWeek != None:
			self.update_activity_tableView(self.database, self.selectedIA, self.currentWeek)

	def on_calendar_select(self):
		selectedDay = self.activity_calendar.selectedDate()
		self.currentWeek = selectedDay.weekNumber()
		if self.selectedIA != None:
			self.update_activity_tableView(self.database, self.selectedIA, self.currentWeek)

	def update_activity_IA_list(self, data):
		#get info from DB
		self.activity_IAs_list = self.findChild(QtWidgets.QListView, "Activity_IAsList")
		model = QtGui.QStandardItemModel()
		self.activity_IAs_list.setModel(model)
		for ia in data["IAs"]:
			model.appendRow(QtGui.QStandardItem(data["IAs"][ia]["name"]))

	def on_activity_table_dataChange(self, index):
		#print('data changed in activity table @', index.column())
		# check user input
		userInput = self.activity_model.itemFromIndex(index)
		if not userInput.text().isnumeric():
			userInput.clearData()
			alert = QtWidgets.QMessageBox()
			alert.setText("error - Input can only be numbers")
			alert.exec_()
		else:
			# get IA's ID from his name
			ia_ID = IngAffaire.getIngAffaireIDfromName(self.selectedIA, self.database)
			print("ia_ID @ on_activity_table_dataChange",ia_ID)
			ia_data = IngAffaire.getIngAffaireFromID(ia_ID, self.database)
			ia = IngAffaire(ia_data["name"], ia_data["role"], ia_ID)
			ia.addAllActivities(ia_data['activities'])
			l = []
			for i in range(self.activity_model.columnCount()):
				if self.activity_model.item(0, i) != None:
					l.append(str(self.activity_model.item(0, i).text()))
			ia.addActivity(str(self.currentWeek[0])+"_"+str(self.currentWeek[1]), l)
			ia.save(self.database)



