from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.Diag_addIA_Window import Diag_addIA_Window
from Classes.Diag_addING_Window import Diag_addING_Window
from Classes.Diag_business_ING_startMission import Diag_business_ING_startMission
from Classes.Diag_business_ING_stopMission import Diag_business_ING_stopMission
from Classes.Diag_delete_ing_ia import Diag_delete_ing_ia

from Classes.IngAffaire import IngAffaire
from Classes.ING import ING


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

		# ADM Business Engineer table
		self.IAs_list = self.findChild(QtWidgets.QTableView, "IAsList")
		# ADM Engineer table
		self.INGs_list = self.findChild(QtWidgets.QTableView, "INGsList")
		self.INGs_list.clicked.connect(self.on_Ings_list_selected)

		# PushButton Action
		self.addNew_IA = self.findChild(QtWidgets.QPushButton, "addNewIA")
		self.addNew_IA.clicked.connect(self.on_addNew_IA)
		self.addNew_ING = self.findChild(QtWidgets.QPushButton, "addNewING")
		self.addNew_ING.clicked.connect(self.on_addNew_ING)


		self.remove_ING = self.findChild(QtWidgets.QPushButton, "delete_ing_pushbutton")
		self.remove_ING.clicked.connect(self.on_remove_Ing)
		self.remove_ING.setEnabled(False)

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
		self.update_IA_tableView(self.database.getContent())
		self.update_ING_tableView(self.database.getContent())

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

		#
		#	tab : Business
		#

		# get current Month info
		self.business_current_date_selector = self.findChild(QtWidgets.QDateEdit, "business_current_month_select")
		self.business_current_date_selector.dateChanged.connect(self.on_business_date_changed)
		self.business_current_date = self.business_current_date_selector.date()

		# setup pushbutton callback
		self.ingStartMission = self.findChild(QtWidgets.QPushButton, "ingStartMission")
		self.ingStartMission.clicked.connect(self.on_business_ingStartMission)
		self.ingStopMission = self.findChild(QtWidgets.QPushButton, "ingStopMission")
		self.ingStopMission.clicked.connect(self.on_business_ingStopMission)

		# setup Business Mission & ingenieur Monthly QtableView
		self.business_Mission_model = QtGui.QStandardItemModel()
		self.business_ingIO_model = QtGui.QStandardItemModel()

		self.business_Mission_model.setColumnCount(4)
		self.business_ingIO_model.setColumnCount(4)
		horizontalHeaders = ["Start", "Total", "Stop", "total"]
		for i, h in enumerate(horizontalHeaders):
			self.business_Mission_model.setHeaderData(i, QtCore.Qt.Horizontal, h)
			self.business_ingIO_model.setHeaderData(i, QtCore.Qt.Horizontal, h)

		verticalHeaderLabels = self.util_getWeeknumbers()
		self.business_Mission_model.setVerticalHeaderLabels(verticalHeaderLabels)
		self.business_ingIO_model.setVerticalHeaderLabels(verticalHeaderLabels)
		self.update_business_Mission(database.getContent())
		self.update_business_ingIO(database.getContent())

		# setup ING list view model
		self.INGs_list_model = QtGui.QStandardItemModel()
		self.INGs_list_model.setColumnCount(1)
		self.INGs_list_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")

		# populate ING list in QtableView
		self.business_Ing_list = self.findChild(QtWidgets.QTableView, "business_Ing_list")
		self.business_Ing_list.clicked.connect(self.on_business_Ingselected)
		self.update_business_ING_listView(self.database.getContent())

		# display window
		self.show()


	def on_addNew_IA(self):
		self.add_IA_Diag = Diag_addIA_Window("./sources/views/add_IA_Diag.ui", self.database, self)

	def on_addNew_ING(self):
		self.add_ING_Diag = Diag_addING_Window("./sources/views/add_ING_Diag.ui", self.database, self)

	def on_remove_Ing(self):
		self.remove_ING_Diag = Diag_delete_ing_ia("./sources/Views/deleteING_IA.ui", self.selectedIng, self.database, self)

	def update_IA_tableView(self, data):
		# get info from DB

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
		self.INGs_model.clear()
		for colID, ING in enumerate(data["INGs"]):
			name = QtGui.QStandardItem(data["INGs"][ING]["name"])
			self.INGs_model.setItem(colID, 0, name)
		self.INGs_list.setModel(self.INGs_model)

	def update_activity_tableView(self, data, IA_name, week_year):
		self.activity_list = self.findChild(QtWidgets.QTableView, "activityList")

		# get IA's ID from his name
		ia_ID = IngAffaire.getIngAffaireIDfromName(self.selectedIA, self.database)
		ia_data = IngAffaire.getIngAffaireFromID(ia_ID, self.database)
		ia = IngAffaire(ia_data["name"], ia_data["role"], ia_ID)

		activities = ia.getActivitiesFromWeek(self.database, str(self.currentWeek[0])+"_"+str(self.currentWeek[1]))

		for i in range(self.activity_model.columnCount()):
			item =  QtGui.QStandardItem(str(activities[i]))
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			self.activity_model.setItem(0, i, item)

		self.activity_list.setModel(self.activity_model)

	def on_Ings_list_selected(self):
		self.selectedIng = self.INGs_list.currentIndex().data()
		self.remove_ING.setEnabled(True)

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
			ia_data = IngAffaire.getIngAffaireFromID(ia_ID, self.database)
			ia = IngAffaire(ia_data["name"], ia_data["role"], ia_ID)
			ia.addAllActivities(ia_data['activities'])
			l = []
			for i in range(self.activity_model.columnCount()):
				if self.activity_model.item(0, i) != None:
					l.append(str(self.activity_model.item(0, i).text()))
			ia.addActivity(str(self.currentWeek[0])+"_"+str(self.currentWeek[1]), l)
			ia.save(self.database)

	def on_business_Ingselected(self):
		self.business_Ing_selected = self.business_Ing_list.currentIndex().data()
		# check ing state
		ing_id = ING.getIngIDfromName(self.business_Ing_selected, self.database)
		content = self.database.getContent()
		if content['INGs'][ing_id]['state'] == "with Mission":
			self.ingStopMission.setEnabled(True)
			self.ingStartMission.setEnabled(False)
		else:
			self.ingStartMission.setEnabled(True)
			self.ingStopMission.setEnabled(False)

	def update_business_ING_listView(self, content):
		self.business_Ing_list.setModel(self.INGs_list_model)
		self.INGs_list_model.clear()
		for colID, ING in enumerate(content["INGs"]):
			name = QtGui.QStandardItem(content["INGs"][ING]["name"])
			if content["INGs"][ING]["state"] == "with Mission":
				name.setBackground(QtGui.QBrush(QtCore.Qt.green))
			else:
				name.setBackground(QtGui.QBrush(QtCore.Qt.red))
			self.INGs_list_model.setItem(colID, 0, name)

	def update_business_ingIO(self, content):
		self.business_ingIO = self.findChild(QtWidgets.QTableView, "business_ing_IO")
		header = self.business_ingIO.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.populate_ing_business_ingIO()
		self.business_ingIO.setModel(self.business_ingIO_model)

	def populate_ing_business_ingIO(self, ing_id=None):
		# add only one ing in table
		currentYear = self.business_current_date.weekNumber()[1]
		if ing_id != None:
			content = self.database.getContent()
			for i in range(self.business_ingIO_model.rowCount()):
				entryDate = QtCore.QDate.fromString(content['INGs'][str(ing_id)]['entryDate'], "dd.MM.yyyy")
				if self.business_ingIO_model.verticalHeaderItem(i).text() == str(entryDate.weekNumber()[0]) and currentYear == entryDate.weekNumber()[1]:
					itemAtWeekNumber = self.business_ingIO_model.item(i, 0)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ", " + content['INGs'][str(ing_id)]["name"]
					else:
						cellContentText = content['INGs'][str(ing_id)]["name"]
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
					self.business_ingIO_model.setItem(i, 0, newIngItem)
					cellContent = self.business_ingIO_model.item(i,0)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_ingIO_model.setItem(i, 1,  QtGui.QStandardItem(str(totalNewIng)))
					return
		# redraw all table if ing_id != None
		content = self.database.getContent()
		# get data from working ING
		for ing in content['INGs']:
			for i in range(self.business_ingIO_model.rowCount()):
				entryDate = QtCore.QDate.fromString(content['INGs'][ing]['entryDate'], "dd.MM.yyyy")
				if self.business_ingIO_model.verticalHeaderItem(i).text() == str(entryDate.weekNumber()[0]) and currentYear == entryDate.weekNumber()[1]:
					# get previous data in cell
					itemAtWeekNumber = self.business_ingIO_model.item(i, 0)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ",\n" + content['INGs'][ing]["name"]
					else:
						cellContentText = content['INGs'][ing]["name"]
					# add new
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
					self.business_ingIO_model.setItem(i, 0, newIngItem)
					cellContent = self.business_ingIO_model.item(i,0)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_ingIO_model.setItem(i, 1,  QtGui.QStandardItem(str(totalNewIng)))
		# get data from archive
		for ing in content["archive"]["INGs"]:
			for i in range(self.business_ingIO_model.rowCount()):
				entryDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]['entryDate'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]['endContract'], "dd.MM.yyyy")
				if self.business_ingIO_model.verticalHeaderItem(i).text() == str(entryDate.weekNumber()[0]) and currentYear == entryDate.weekNumber()[1]:
					# get previous data in cell
					itemAtWeekNumber = self.business_ingIO_model.item(i, 0)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ",\n" + content["archive"]['INGs'][ing]["name"]
					else:
						cellContentText = content["archive"]['INGs'][ing]["name"]
					# add new
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
					self.business_ingIO_model.setItem(i, 0, newIngItem)
					cellContent = self.business_ingIO_model.item(i,0)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_ingIO_model.setItem(i, 1,  QtGui.QStandardItem(str(totalNewIng)))
				if self.business_ingIO_model.verticalHeaderItem(i).text() == str(exitDate.weekNumber()[0]) and currentYear == entryDate.weekNumber()[1]:
					# get previous data in cell
					itemAtWeekNumber = self.business_ingIO_model.item(i, 0)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ",\n" + content["archive"]['INGs'][ing]["name"]
					else:
						cellContentText = content["archive"]['INGs'][ing]["name"]
					# add new
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.red))
					self.business_ingIO_model.setItem(i, 2, newIngItem)
					cellContent = self.business_ingIO_model.item(i,2)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_ingIO_model.setItem(i, 3,  QtGui.QStandardItem(str(totalNewIng)))

	def populate_ing_business_MissionIO(self, ing_id=None):


		currentYear = self.business_current_date.weekNumber()[1]
		content = self.database.getContent()

		if ing_id != None:
			# find cell where Ing name is
			ingName = content["INGs"][ing_id]['name']
			for i in range(self.business_Mission_model.rowCount()):
				itemAtWeekNumber = self.business_Mission_model.item(i, 0)
				if itemAtWeekNumber != None and itemAtWeekNumber.text().find(ingName) != -1:
					print ('Founded')
					return
		for ing in content['INGs']:
			for i in range(self.business_Mission_model.rowCount()):
				entryDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Start'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Stop'], "dd.MM.yyyy")
				if self.business_Mission_model.verticalHeaderItem(i).text() == str(entryDate.weekNumber()[0]) and currentYear == entryDate.weekNumber()[1]:
					# get previous data in cell
					itemAtWeekNumber = self.business_Mission_model.item(i, 0)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ",\n" + content['INGs'][ing]["name"]
					else:
						cellContentText = content['INGs'][ing]["name"]
					# add new
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
					self.business_Mission_model.setItem(i, 0, newIngItem)
					cellContent = self.business_Mission_model.item(i,0)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_Mission_model.setItem(i, 1,  QtGui.QStandardItem(str(totalNewIng)))
				if self.business_Mission_model.verticalHeaderItem(i).text() == str(exitDate.weekNumber()[0]) and currentYear == exitDate.weekNumber()[1]:
					# get previous data in cell
					itemAtWeekNumber = self.business_Mission_model.item(i, 2)
					if itemAtWeekNumber != None:
						cellContentText = itemAtWeekNumber.text() + ",\n" + content['INGs'][ing]["name"]
					else:
						cellContentText = content['INGs'][ing]["name"]
					# add new
					newIngItem = QtGui.QStandardItem( cellContentText )
					newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.red))
					self.business_Mission_model.setItem(i, 2, newIngItem)
					cellContent = self.business_Mission_model.item(i, 2)
					if cellContent != None:
						totalNewIng = len(cellContent.text().split(','))
						self.business_Mission_model.setItem(i, 3,  QtGui.QStandardItem(str(totalNewIng)))

	def update_business_Mission(self, content):
		self.business_Mission = self.findChild(QtWidgets.QTableView, "business_mission_start_stop")
		header = self.business_Mission.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.populate_ing_business_MissionIO()
		self.business_Mission.setModel(self.business_Mission_model)

	def on_business_ingStartMission(self):
		self.diag_business_startMission = Diag_business_ING_startMission("./sources/views/ing_start_mission.ui", self.business_Ing_selected, self.database, self)
		self.update_business_ING_listView(self.database.getContent())

	def on_business_ingStopMission(self):
		self.diag_business_stopMission = Diag_business_ING_stopMission("./sources/views/ing_stop_mission.ui", self.business_Ing_selected, self.database, self)
		self.update_business_ING_listView(self.database.getContent())

	def util_getWeeknumbers(self):
		self.business_current_date = self.business_current_date_selector.date()
		verticalHeaderLabels = []
		for i in range (-1, 2):
			tmpDate = QtCore.QDate(self.business_current_date.year(), self.business_current_date.month() + i, 1)
			nbrDayInMonth = tmpDate.daysInMonth()
			weekCount = nbrDayInMonth / 7
			i = 0
			while weekCount > 0:
				if str(tmpDate.weekNumber()[0] + i) not in verticalHeaderLabels:
					verticalHeaderLabels.append(str(tmpDate.weekNumber()[0] + i))
				weekCount -= 1
				i += 1

		return verticalHeaderLabels

	def on_business_date_changed(self):
		self.business_Mission_model.clear()
		self.business_ingIO_model.clear()

		self.business_Mission_model.setColumnCount(4)
		self.business_ingIO_model.setColumnCount(4)
		horizontalHeaders = ["Start", "Total", "Stop", "total"]
		for i, h in enumerate(horizontalHeaders):
			self.business_Mission_model.setHeaderData(i, QtCore.Qt.Horizontal, h)
			self.business_ingIO_model.setHeaderData(i, QtCore.Qt.Horizontal, h)

		verticalHeaderLabel = self.util_getWeeknumbers()

		self.business_Mission_model.setVerticalHeaderLabels(verticalHeaderLabel)
		self.business_ingIO_model.setVerticalHeaderLabels(verticalHeaderLabel)
		self.update_business_Mission(self.database.getContent())
		self.update_business_ingIO(self.database.getContent())