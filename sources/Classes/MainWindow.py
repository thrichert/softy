from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.Diag_addIA_Window import Diag_addIA_Window
from Classes.Diag_addING_Window import Diag_addING_Window
from Classes.Diag_business_ING_startMission import Diag_business_ING_startMission
from Classes.Diag_business_ING_stopMission import Diag_business_ING_stopMission
from Classes.Diag_delete_ing_ia import Diag_delete_ing_ia
from Classes.Diag_addBU_Window import Diag_addBU_Window

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
		self.today = QtCore.QDate.currentDate()

		# check data
		self.verifyData()

		#================================================
		#	tab : ADM
		#================================================

		# ADM Business Engineer table
		self.IAs_list = self.findChild(QtWidgets.QTableView, "IAsList")
		header = self.IAs_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		# ADM Engineer table
		self.INGs_list = self.findChild(QtWidgets.QTableView, "INGsList")
		self.INGs_list.clicked.connect(self.on_Ings_list_selected)
		header = self.INGs_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		# PushButton Action
		self.addNew_IA = self.findChild(QtWidgets.QPushButton, "addNewIA")
		self.addNew_IA.clicked.connect(self.on_addNew_IA)
		self.addNew_ING = self.findChild(QtWidgets.QPushButton, "addNewING")
		self.addNew_ING.clicked.connect(self.on_addNew_ING)


		self.addNew_Bu = self.findChild(QtWidgets.QPushButton, "addNewBU")
		self.addNew_Bu.clicked.connect(self.on_addNew_BU)

		self.remove_ING = self.findChild(QtWidgets.QPushButton, "delete_ing_pushbutton")
		self.remove_ING.clicked.connect(self.on_remove_Ing)
		self.remove_ING.setEnabled(False)


		# setup Bu Qtableview
		self.Bus_listView = self.findChild(QtWidgets.QTableView, "BUsList")
		self.BUs_model = QtGui.QStandardItemModel()
		self.BUs_model.setColumnCount(1)
		self.BUs_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Name')
		header = self.Bus_listView.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)


		# setup IAs QtableView
		self.IAs_model = QtGui.QStandardItemModel()
		self.IAs_model.setColumnCount(3)
		self.IAs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
		self.IAs_model.setHeaderData(1, QtCore.Qt.Horizontal, "Role")
		self.IAs_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Business Unit')

		# setup INGs QtableView
		self.INGs_model = QtGui.QStandardItemModel()
		self.INGs_model.setColumnCount(1)
		self.INGs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")




		#================================================
		#	tab : activite
		#================================================

		self.currentWeek = None
		self.selectedIA = None

		# calendar callback on day select
		self.activity_calendar = self.findChild(QtWidgets.QCalendarWidget, "activityCalendar")
		self.activity_calendar.clicked.connect(self.on_calendar_select)

		# get BU selector

		self.activity_detailBU_selector = self.findChild(QtWidgets.QComboBox, "detail_BU_comboBox")
		self.activity_globalBU_selector = self.findChild(QtWidgets.QComboBox, "global_BU_comboBox")

		self.activity_detailBU_selector.currentIndexChanged.connect(self.update_activity_IA_list)

		# setup IAs list
		self.update_activity_IA_list()
		self.activity_IAs_list.clicked.connect(self.on_activity_IAselected)

		# setup activity QtableView
		self.activity_model = QtGui.QStandardItemModel()
		self.activity_model.setColumnCount(10)
		headers = ["Prosp", "Nvx Besoin","Besoins Actifs", "KLIF", "START", "Push DC", "EC1", "EC2", "PPLES", "RH+"]
		for i, h in enumerate(headers):
			self.activity_model.setHeaderData(i, QtCore.Qt.Horizontal, h)
		self.activity_model.insertRow(0)
		self.activity_model.dataChanged.connect(self.on_activity_table_dataChange)


		# setup label in tx de tranfert
		self.activity_metrics_tx_tranfo = [None for i in range (5)]
		self.activity_metrics_tx_tranfo[0] = self.findChild(QtWidgets.QLabel, "ia_Besoin_per_Prosp")
		self.activity_metrics_tx_tranfo[1] = self.findChild(QtWidgets.QLabel, "ia_RT_per_Besoin")
		self.activity_metrics_tx_tranfo[2] = self.findChild(QtWidgets.QLabel, "ia_Rplus_per_RT")
		self.activity_metrics_tx_tranfo[3] = self.findChild(QtWidgets.QLabel, "ia_EC2_per_EC1")
		self.activity_metrics_tx_tranfo[4] = self.findChild(QtWidgets.QLabel, "ia_RHPLUS_per_EC1")
		self.activity_metrics_tx_transfo_objectif = [None for i in range(5)]
		self.activity_metrics_tx_transfo_objectif[0] = self.findChild(QtWidgets.QLabel, "ia_obj_Besoin_per_Prosp")
		self.activity_metrics_tx_transfo_objectif[1] = self.findChild(QtWidgets.QLabel, "ia_obj_RT_per_Besoin")
		self.activity_metrics_tx_transfo_objectif[2] = self.findChild(QtWidgets.QLabel, "ia_obj_Rplus_per_RT")
		self.activity_metrics_tx_transfo_objectif[3] = self.findChild(QtWidgets.QLabel, "ia_obj_EC2_per_EC1")
		self.activity_metrics_tx_transfo_objectif[4] = self.findChild(QtWidgets.QLabel, "ia_obj_RHPLUS_per_EC1")


		#================================================
		#	tab : Business
		#================================================

		# get Bu selector element
		self.business_BuSelector = self.findChild(QtWidgets.QComboBox, "business_BuComboBox")
		self.business_BuSelector.currentIndexChanged.connect(self.on_business_BU_selected)
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
		self.business_ing_table_model = None
		self.update_business_ing_table()

		# setup ING list view model
		self.INGs_list_model = QtGui.QStandardItemModel()
		self.INGs_list_model.setColumnCount(1)
		self.INGs_list_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")

		# populate ING list in QtableView
		self.business_Ing_list = self.findChild(QtWidgets.QTableView, "business_Ing_list")
		self.business_Ing_list.clicked.connect(self.on_business_Ingselected)
		self.update_business_ING_listView()

		# ADM
		# populate list in QtableViews
		self.update_IA_tableView()
		self.update_ING_tableView()
		self.update_BU_tableView()

		# Activity
		# populate BU selector
		self.update_activity_BuComboBox()

		# Business
		# popuplate BU Selector
		self.update_business_BuComboBox()

		# display window
		self.show()

	def on_addNew_BU(self):
		self.add_BU_Diag = Diag_addBU_Window("./sources/views/add_BU_Diag.ui", self.database)
		self.update_BU_tableView()
		self.update_activity_BuComboBox()
		self.update_business_BuComboBox()

	def on_addNew_IA(self):
		self.add_IA_Diag = Diag_addIA_Window("./sources/views/add_IA_Diag.ui", self.database)
		self.update_IA_tableView()

	def on_addNew_ING(self):
		self.add_ING_Diag = Diag_addING_Window("./sources/views/add_ING_Diag.ui", self.database)
		self.update_ING_tableView()
		self.update_business_ING_listView()
		self.update_business_ing_table()

	def on_remove_Ing(self):
		self.remove_ING_Diag = Diag_delete_ing_ia("./sources/Views/deleteING_IA.ui", self.selectedIng, self.database)
		# update Views
		self.update_ING_tableView()
		self.update_business_ING_listView()
		self.update_business_ing_table()

	def update_BU_tableView(self):
		content = self.database.getContent()
		for rowID, Bu in enumerate(content["BUs"]):
			self.BUs_model.setItem(rowID, 0, QtGui.QStandardItem(Bu))
		# update Others Combo Box

		# set model in view
		self.Bus_listView.setModel(self.BUs_model)

	def update_IA_tableView(self):
		# get info from DB
		content = self.database.getContent()

		self.IAs_list.setModel(self.IAs_model)
		for rowID, IA in enumerate(content["IAs"]):
			name = QtGui.QStandardItem(content["IAs"][IA]["name"])
			role = QtGui.QStandardItem(content["IAs"][IA]["role"])
			bu = QtGui.QStandardItem(content["IAs"][IA]["BU"])
			self.IAs_model.setItem(rowID, 0, name)
			self.IAs_model.setItem(rowID, 1, role)
			self.IAs_model.setItem(rowID, 2, bu)
		self.update_activity_IA_list()

	def update_ING_tableView(self):
		content = self.database.getContent()
		self.INGs_model.clear()
		for colID, ING in enumerate(content["INGs"]):
			name = QtGui.QStandardItem(content["INGs"][ING]["name"])
			self.INGs_model.setItem(colID, 0, name)
		self.INGs_list.setModel(self.INGs_model)

	def update_activity_tableView(self, data, IA_name, week_year):
		self.activity_list = self.findChild(QtWidgets.QTableView, "activityList")

		# get IA's ID from his name
		ia_ID = IngAffaire.getIngAffaireIDfromName(self.selectedIA, self.database)
		ia_data = IngAffaire.getIngAffaireFromID(ia_ID, self.database)
		ia = IngAffaire(name=ia_data["name"], role=ia_data["role"], idx=ia_ID)

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
		ia_ID = IngAffaire.getIngAffaireIDfromName(self.selectedIA, self.database)
		ia = IngAffaire(idx=ia_ID).loadFromDB(self.database)
		self._activity_update_metrics(ia)

	def update_activity_BuComboBox(self):
		content = self.database.getContent()
		for i, bu in enumerate(content["BUs"]):
			self.activity_detailBU_selector.insertItem(i, bu)
			self.activity_globalBU_selector.insertItem(i, bu)

	def update_business_BuComboBox(self):
		content = self.database.getContent()
		for i, bu in enumerate(content["BUs"]):
			self.business_BuSelector.insertItem(i, bu)

	def on_calendar_select(self):
		selectedDay = self.activity_calendar.selectedDate()
		self.currentWeek = selectedDay.weekNumber()
		if self.selectedIA != None:
			self.update_activity_tableView(self.database, self.selectedIA, self.currentWeek)

	def update_activity_IA_list(self):
		content = self.database.getContent()
		#get current selected BU
		selectedBU = self.activity_detailBU_selector.currentText()
		self.activity_IAs_list = self.findChild(QtWidgets.QListView, "Activity_IAsList")
		model = QtGui.QStandardItemModel()
		self.activity_IAs_list.setModel(model)
		for ia in content["IAs"]:
			if content["IAs"][ia]["BU"] == selectedBU:
				model.appendRow(QtGui.QStandardItem(content["IAs"][ia]["name"]))

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
			ia = IngAffaire(idx=ia_ID).loadFromDB(self.database)
			if ia == None:
				alert = QtWidgets.QMessageBox()
				alert.setText("error - " + self.selectedIA + "Not find in database...")
				alert.exec_()
				return

			l = []
			for i in range(self.activity_model.columnCount()):
				if self.activity_model.item(0, i) != None:
					cellContent = self.activity_model.item(0, i).text()
					if cellContent == "":
						cellContent = 0
					else:
						l.append(str(cellContent))
				else:
					l.append(str(0))
			ia.addActivity(str(self.currentWeek[0])+"_"+str(self.currentWeek[1]), l)
			ia.processMetrics()
			ia.save(self.database)
			# update metrics
			self._activity_update_metrics(ia)

	def _activity_update_metrics(self, ia):
		res = ia.getTxTransfo(self.database)
		for i in range (5):
		 	self.activity_metrics_tx_tranfo[i].setText("{:.2f}%".format(res[i] * 100))
		# 	if res[i] * 100 > float(self.activity_metrics_tx_transfo_objectif[i].text()):
		# 		#objectName = self.activity_metrics_tx_transfo[i]
		# 		#self.activity_metrics_tx_tranfo[i].setStyleSheet('QLabel#nom_plan_label {color: yellow}')
		# 		pass

	def init_business_table(self, table_model = None):
		if table_model != None:
			table_model.clear()
		else:
			table_model = QtGui.QStandardItemModel()

		horizontalHeaders = ["Ing In", "Total", "Ing Out", "total", "Start", "Total", "Stop", "Total"]
		table_model.setColumnCount(len(horizontalHeaders))
		for i, h in enumerate(horizontalHeaders):
			table_model.setHeaderData(i, QtCore.Qt.Horizontal, h)

		table_model.setVerticalHeaderLabels(self.util_getWeeknumbers())
		self.business_ing_table = self.findChild(QtWidgets.QTableView, "business_ing_table")
		header = self.business_ing_table.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

		self.business_ing_table.setModel(table_model)
		return table_model

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

	def update_business_ING_listView(self):
		content = self.database.getContent()
		self.business_Ing_list.setModel(self.INGs_list_model)
		self.INGs_list_model.clear()
		today = QtCore.QDate.currentDate()
		for colID, ING in enumerate(content["INGs"]):
			if content["INGs"][ING]["BU"] == self.business_BuSelector.currentText():
				name = QtGui.QStandardItem(content["INGs"][ING]["name"])
				stopMissionDate = QtCore.QDate().fromString(content["INGs"][ING]["mission_Stop"], "dd.MM.yyyy")

				if content["INGs"][ING]["state"] == "with Mission" and today.daysTo(stopMissionDate) > 3:
					name.setBackground(QtGui.QBrush(QtCore.Qt.green))
				elif content["INGs"][ING]["state"] == "with Mission" and today.daysTo(stopMissionDate) <= 3:
					name.setBackground(QtGui.QBrush(QtCore.Qt.yellow))
				else:
					name.setBackground(QtGui.QBrush(QtCore.Qt.red))
				self.INGs_list_model.setItem(colID, 0, name)

	def update_business_ing_table(self):
		if self.business_ing_table_model != None:
			self.business_ing_table_model.clear()
		self.business_ing_table_model = self.init_business_table()
		self.populate_ing_business_ingIO()
		self.populate_ing_business_MissionIO()
		self.business_ing_table.setModel(self.business_ing_table_model)

	def _add_ing_enter_ingIO(self, ingData, rowIndex):
		#	get previous data in cell
		itemAtWeekNumber = self.business_ing_table_model.item(rowIndex, 0)
		if itemAtWeekNumber != None:
			cellContentText = itemAtWeekNumber.text() + ",\n" + ingData["name"]
		else:
			cellContentText = ingData["name"]
		# add new
		newIngItem = QtGui.QStandardItem( cellContentText )
		newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
		self.business_ing_table_model.setItem(rowIndex, 0, newIngItem)
		cellContent = self.business_ing_table_model.item(rowIndex, 0)
		if cellContent != None:
			totalNewIng = len(cellContent.text().split(','))
			self.business_ing_table_model.setItem(rowIndex, 1,  QtGui.QStandardItem(str(totalNewIng)))

	def _add_ing_exit_ingIO(self, ingData, rowIndex):
		#	get previous data in cell
		itemAtWeekNumber = self.business_ing_table_model.item(rowIndex, 2)
		if itemAtWeekNumber != None:
			cellContentText = itemAtWeekNumber.text() + ",\n" + ingData["name"]
		else:
			cellContentText = ingData["name"]
		# add new
		newIngItem = QtGui.QStandardItem( cellContentText )
		newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.red))
		self.business_ing_table_model.setItem(rowIndex, 2, newIngItem)
		cellContent = self.business_ing_table_model.item(rowIndex, 2)
		if cellContent != None:
			totalNewIng = len(cellContent.text().split(','))
			self.business_ing_table_model.setItem(rowIndex, 3,  QtGui.QStandardItem(str(totalNewIng)))

	def populate_ing_business_ingIO(self):
		currentYear = self.business_current_date.weekNumber()[1]
		content = self.database.getContent()
		currentBU = self.business_BuSelector.currentText()
		for ing in content["INGs"]:
			if content["INGs"][ing]["BU"] == currentBU:
				entryDate = QtCore.QDate.fromString(content['INGs'][ing]['entryDate'], "dd.MM.yyyy")

				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = entryDate.weekNumber()[1]
				for i in range(self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					if currentRowVerticalHeader == entryDateWeekNbr and currentYear == entryDateYearNbr:
						self._add_ing_enter_ingIO(content["INGs"][ing], i)

		for ing in content['archive']["INGs"]:
			if content['archive']["INGs"][ing]["BU"] == currentBU:
				entryDate = QtCore.QDate.fromString(content['archive']["INGs"][ing]['entryDate'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content['archive']["INGs"][ing]['endContract'], "dd.MM.yyyy")
				exitDateWeekNbr = str(exitDate.weekNumber()[0])
				exitDateYearNbr = exitDate.weekNumber()[1]
				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = entryDate.weekNumber()[1]
				for i in range(self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					if currentRowVerticalHeader == entryDateWeekNbr and currentYear == entryDateYearNbr:
						self._add_ing_enter_ingIO(content['archive']["INGs"][ing], i)
					if currentRowVerticalHeader == exitDateWeekNbr and currentYear == exitDateYearNbr:
						self._add_ing_exit_ingIO(content['archive']["INGs"][ing], i)

	def _add_ing_start_mission(self, ingData, rowIndex):
		#	get previous data in cell
		itemAtWeekNumber = self.business_ing_table_model.item(rowIndex, 4)
		if itemAtWeekNumber != None:
			cellContentText = itemAtWeekNumber.text() + ",\n" + ingData["name"]
		else:
			cellContentText = ingData["name"]
		# add new
		newIngItem = QtGui.QStandardItem( cellContentText )
		newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.green))
		self.business_ing_table_model.setItem(rowIndex, 4, newIngItem)
		cellContent = self.business_ing_table_model.item(rowIndex, 4)
		if cellContent != None:
			totalNewIng = len(cellContent.text().split(','))
			self.business_ing_table_model.setItem(rowIndex, 5,  QtGui.QStandardItem(str(totalNewIng)))

	def _add_ing_stop_mission(self, ingData, rowIndex):
		itemAtWeekNumber = self.business_ing_table_model.item(rowIndex, 6)
		if itemAtWeekNumber != None:
			cellContentText = itemAtWeekNumber.text() + ",\n" + ingData["name"]
		else:
			cellContentText = ingData["name"]
		# add new
		newIngItem = QtGui.QStandardItem( cellContentText )
		newIngItem.setBackground(QtGui.QBrush(QtCore.Qt.red))
		self.business_ing_table_model.setItem(rowIndex, 6, newIngItem)
		cellContent = self.business_ing_table_model.item(rowIndex, 6)
		if cellContent != None:
			totalNewIng = len(cellContent.text().split(','))
			self.business_ing_table_model.setItem(rowIndex, 7,  QtGui.QStandardItem(str(totalNewIng)))

	def populate_ing_business_MissionIO(self, ing_id=None):
		currentYear = self.business_current_date.weekNumber()[1]
		content = self.database.getContent()
		for ing in content["INGs"]:
			entryDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Start'], "dd.MM.yyyy")
			exitDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Stop'], "dd.MM.yyyy")

			entryDateWeekNbr = str(entryDate.weekNumber()[0])
			entryDateYearNbr = entryDate.weekNumber()[1]

			exitDateWeekNbr = str(exitDate.weekNumber()[0])
			exitDateYearNbr = exitDate.weekNumber()[1]

			for i in range (self.business_ing_table_model.rowCount()):
				currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
				if currentRowVerticalHeader == entryDateWeekNbr and currentYear == entryDateYearNbr:
					self._add_ing_start_mission(content["INGs"][ing], i)
				if  currentRowVerticalHeader == exitDateWeekNbr and currentYear == exitDateYearNbr:
					self._add_ing_stop_mission(content["INGs"][ing], i)

	def on_business_ingStartMission(self):
		self.diag_business_startMission = Diag_business_ING_startMission("./sources/views/ing_start_mission.ui", self.business_Ing_selected, self.database)
		self.update_business_ING_listView()
		self.update_business_ing_table()

	def on_business_ingStopMission(self):
		self.diag_business_stopMission = Diag_business_ING_stopMission("./sources/views/ing_stop_mission.ui", self.business_Ing_selected, self.database)
		self.update_business_ING_listView()
		self.update_business_ing_table()

	def on_business_BU_selected(self):
		self.update_business_ING_listView()
		self.update_business_ing_table()
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
		self.business_ing_table_model.clear()
		self.business_ing_table_model = self.init_business_table()
		# populate table
		self.populate_ing_business_MissionIO()
		self.populate_ing_business_ingIO()

	def verifyData(self):
		content = self.database.getContent()
		warningIngNames_reset = []
		warningIngNames_3days = []
		for ing in content["INGs"]:
			ingName = content["INGs"][ing]["name"]
			#mission_Start = QtCore.QDate().fromString(content["INGs"][ing]['mission_Start'], "dd.MM.yyyy")
			mission_Stop = QtCore.QDate().fromString(content["INGs"][ing]['mission_Stop'], "dd.MM.yyyy")
			#currentState = content["INGs"][ing]['state']
			if self.today.daysTo(mission_Stop) < 3:
				warningIngNames_3days.append(ingName)
			if self.today.daysTo(mission_Stop) <= 0:
				content["INGs"][ing]["state"] = "without Mission"
				content["INGs"][ing]["current_client"] = ""
				warningIngNames_reset.append(ingName)

		N = len(warningIngNames_3days)
		if N > 0:
			message = "Warning - ["
			for i, name in enumerate(warningIngNames_3days):
				message += name
				if i < N - 1:
					message += ', '
			message += '] will stop their mission in less than 3 day !'
			alert = QtWidgets.QMessageBox()
			alert.setText(message)
			alert.exec_()

		N = len(warningIngNames_reset)
		if N > 0:
			message = "Warning - Automatic Reset for : ["
			for i, name in enumerate(warningIngNames_3days):
				message += name
				if i < N - 1:
					message += ', '
			message += ']'
			alert = QtWidgets.QMessageBox()
			alert.setText(message)
			alert.exec_()


