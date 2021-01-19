from PyQt5 import QtWidgets, uic, QtCore, QtGui
import sys, os, json
from Classes.DB import DB
from Classes.Diag_addIA_Window import Diag_addIA_Window
from Classes.Diag_addING_Window import Diag_addING_Window
from Classes.Diag_business_ING_startMission import Diag_business_ING_startMission
from Classes.Diag_business_ING_stopMission import Diag_business_ING_stopMission
from Classes.Diag_delete_ing_ia import Diag_delete_ing_ia
from Classes.Diag_addBU_Window import Diag_addBU_Window
from Classes.Diag_editING_Window import Diag_editING_Window
from Classes.User import User
from Classes.IngAffaire import IngAffaire
from Classes.ING import ING

def resource_path(relative_path):
	try:
		# PyInstaller creates a temp folder and stores path in _MEIPASS
		base_path = sys._MEIPASS
	except Exception:
		base_path = os.path.abspath(".")

	return os.path.join(base_path, relative_path)


class MainWindow(QtWidgets.QMainWindow):
	"""
	Class that handle the main window
	"""

	__PATH_MAINWINDOW_UI	= resource_path("views\\mainWindow.ui")
	__PATH_ADDBU_UI			= resource_path("views\\add_BU_Diag.ui")
	__PATH_ADDIA_UI			= resource_path("views\\add_IA_Diag.ui")
	__PATH_ADDING_UI		= resource_path("views\\add_ING_Diag.ui")
	__PATH_DELUSER_UI		= resource_path("Views\\deleteING_IA.ui")
	__PATH_STARTMISSION_UI	= resource_path("views\\ing_start_mission.ui")
	__PATH_STOPMISSION_UI	= resource_path("views\\ing_stop_mission.ui")
	__PATH_EDITING_UI		= resource_path("views\\edit_ING_Diag.ui")

	def __init__(self, database):
		super(MainWindow, self).__init__()
		uic.loadUi(MainWindow.__PATH_MAINWINDOW_UI, self)
		self.database = database
		self.dbContent = self.database.getContent()


		self.today = QtCore.QDate.currentDate()

		# check data
		self.verifyData()

		#================================================
		#	tab : ADM
		#================================================

		# ADM Bu Qtableview
		self.Bus_list = self.findChild(QtWidgets.QTableView, "BUsList")
		self.Bus_list.clicked.connect(self.on_BUs_list_selected)
		header = self.Bus_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.Bus_list.verticalHeader().hide()
		self.Bus_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.Bus_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
		# ADM Business Engineer table
		self.IAs_list = self.findChild(QtWidgets.QTableView, "IAsList")
		self.IAs_list.clicked.connect(self.on_IAs_list_selected)
		header = self.IAs_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.IAs_list.verticalHeader().hide()
		self.IAs_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.IAs_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		# ADM Engineer table
		self.INGs_list = self.findChild(QtWidgets.QTableView, "INGsList")
		self.INGs_list.clicked.connect(self.on_Ings_list_selected)
		header = self.INGs_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.INGs_list.verticalHeader().hide()
		self.INGs_list.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
		self.INGs_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		# PushButton Action

		self.addNew_Bu = self.findChild(QtWidgets.QPushButton, "addNewBU")
		self.addNew_Bu.clicked.connect(self.on_addNew_BU)
		self.addNew_IA = self.findChild(QtWidgets.QPushButton, "addNewIA")
		self.addNew_IA.clicked.connect(self.on_addNew_IA)
		self.addNew_IA.setEnabled(False)
		self.addNew_ING = self.findChild(QtWidgets.QPushButton, "addNewING")
		self.addNew_ING.clicked.connect(self.on_addNew_ING)
		self.addNew_ING.setEnabled(False)

		if len(self.dbContent["BUs"]) != 0:
			self.addNew_IA.setEnabled(True)
			self.addNew_ING.setEnabled(True)

		self.edit_ING = self.findChild(QtWidgets.QPushButton, "edit_ing_pushbutton")
		self.edit_ING.setEnabled(False)
		self.edit_ING.clicked.connect(self.on_edit_ing)

		self.remove_ING = self.findChild(QtWidgets.QPushButton, "delete_ing_pushbutton")
		self.remove_ING.clicked.connect(self.on_remove_Ing)
		self.remove_ING.setEnabled(False)

		self.remove_IA = self.findChild(QtWidgets.QPushButton, "delete_ia_pushbutton")
		self.remove_IA.clicked.connect(self.on_remove_IA)
		self.remove_IA.setEnabled(False)

		self.remove_BU = self.findChild(QtWidgets.QPushButton, "delete_bu_pushbutton")
		self.remove_BU.clicked.connect(self.on_remove_BU)
		self.remove_BU.setEnabled(False)

		# setup BUs QtableView
		self.BUs_model = QtGui.QStandardItemModel()
		self.BUs_model.setColumnCount(1)
		self.BUs_model.setHeaderData(0, QtCore.Qt.Horizontal, 'Name')
		self.Bus_list.setModel(self.BUs_model)


		# setup IAs QtableView
		self.IAs_model = QtGui.QStandardItemModel()
		self.IAs_model.setColumnCount(3)
		self.IAs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
		self.IAs_model.setHeaderData(1, QtCore.Qt.Horizontal, "Role")
		self.IAs_model.setHeaderData(2, QtCore.Qt.Horizontal, 'Business Unit')
		self.IAs_list.setModel(self.IAs_model)

		# setup INGs QtableView
		self.INGs_model = QtGui.QStandardItemModel()
		self.INGs_model.setColumnCount(1)
		self.INGs_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")
		self.INGs_list.setModel(self.INGs_model)

		#init model

		for bu in self.dbContent["BUs"]:
			self.BUs_model.appendRow(QtGui.QStandardItem(bu))
		self.BUs_model.rowsInserted.connect(self._mainViewUpdate)
		self.BUs_model.rowsRemoved.connect(self._mainViewUpdate)

		for ia in self.dbContent["IAs"]:
			r = []
			ia = IngAffaire.load(self.database, self.dbContent["IAs"][ia]["name"])
			r.append(QtGui.QStandardItem(ia.getName()))
			r.append(QtGui.QStandardItem(ia.getRole()))
			r.append(QtGui.QStandardItem(ia.getBu()))
			self.IAs_model.appendRow(r)
		self.IAs_model.rowsInserted.connect(self._mainViewUpdate)
		self.IAs_model.rowsRemoved.connect(self._mainViewUpdate)

		for ing in self.dbContent["INGs"]:
			self.INGs_model.appendRow(QtGui.QStandardItem(self.dbContent["INGs"][ing]["name"]))
		self.INGs_model.rowsInserted.connect(self._mainViewUpdate)
		self.INGs_model.rowsRemoved.connect(self._mainViewUpdate)

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
		self.activity_detailBU_selector.currentIndexChanged.connect(self.update_activity_IAMGR_list)


		# get Manager selector

		self.activity_manager_selector = self.findChild(QtWidgets.QComboBox, "activityManagerList")
		self.activity_manager_selector.currentIndexChanged.connect(self.update_activity_IA_list)


		# setup IAs list
		self.activity_IAs_list = self.findChild(QtWidgets.QTableView, "Activity_IAsList")
		header = self.activity_IAs_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.activity_IAs_list.verticalHeader().hide()
		self.update_activity_IA_list()
		self.activity_IAs_list.clicked.connect(self.on_activity_IAselected)
		self.activity_IAs_list.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)

		# setup activity QtableView
		self.activity_list = self.findChild(QtWidgets.QTableView, "activityList")
		header = self.activity_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.activity_list.verticalHeader().hide()

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
		self.business_ing_table_model = None

		# get Bu selector element
		self.business_BuSelector = self.findChild(QtWidgets.QComboBox, "business_BuComboBox")
		self.business_BuSelector.setModel(self.BUs_model)
		self.business_BuSelector.currentIndexChanged.connect(self.on_business_BU_selected)

		# get Manager selector element
		self.business_managerSelector = self.findChild(QtWidgets.QComboBox, "businessManagerList")
		self.business_managerSelector.currentIndexChanged.connect(self.on_business_manager_selected)

		# get current Month info
		self.business_current_date_selector = self.findChild(QtWidgets.QDateEdit, "business_current_month_select")
		self.business_current_date_selector.dateChanged.connect(self.on_business_date_changed)
		self.business_current_date_selector.setDate(QtCore.QDate().currentDate())
		self.business_current_date = self.business_current_date_selector.date()

		# setup pushbutton callback
		self.ingStartMission = self.findChild(QtWidgets.QPushButton, "ingStartMission")
		self.ingStartMission.clicked.connect(self.on_business_ingStartMission)
		self.ingStopMission = self.findChild(QtWidgets.QPushButton, "ingStopMission")
		self.ingStopMission.clicked.connect(self.on_business_ingStopMission)

		# get totaux text label
		self.business_tot_IngInBU = self.findChild(QtWidgets.QLabel, "IngInBU")
		self.business_tot_IngInMission = self.findChild(QtWidgets.QLabel, "IngInMission")
		self.business_tot_IngActivityRatio = self.findChild(QtWidgets.QLabel, "IngActivityRatio")
		self.update_business_textLabel()

		# setup Business Mission & ingenieur Monthly QtableView
		self.update_business_ing_table()

		# populate ING list in QtableView
		self.business_Ing_list = self.findChild(QtWidgets.QTableView, "business_Ing_list")
		self.business_Ing_list.clicked.connect(self.on_business_Ingselected)
		header = self.business_Ing_list.horizontalHeader()
		header.setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
		self.business_Ing_list.verticalHeader().hide()
		self.business_Ing_list.setItemDelegate(businessIngListDelegate(parent=self))
		self.on_business_BU_selected()
		# Activity
		# populate BU selector
		self.activity_detailBU_selector.setModel(self.BUs_model)

		# Business
		# popuplate BU Selector
		self.activity_globalBU_selector.setModel(self.BUs_model)

		# display window
		self.show()

	def _mainViewUpdate(self):
		self.business_BuSelector.setCurrentIndex(0)
		self.update_activity_IAMGR_list()
		self.on_business_BU_selected()
		self.update_business_ing_table()

	def on_addNew_BU(self):
		self.add_BU_Diag = Diag_addBU_Window(MainWindow.__PATH_ADDBU_UI, self.database)
		if (self.add_BU_Diag.added):
			self.BUs_model.appendRow(QtGui.QStandardItem(self.add_BU_Diag.BuNameText))
			self.addNew_IA.setEnabled(True)
			self.addNew_ING.setEnabled(True)
		self.business_BuSelector.setCurrentIndex(0)

	def on_addNew_IA(self):
		self.add_IA_Diag = Diag_addIA_Window(MainWindow.__PATH_ADDIA_UI, self.database)
		if (self.add_IA_Diag.added):
			#add ia in model
			ia = IngAffaire.load(self.database, self.add_IA_Diag.userNameText)
			r = [ QtGui.QStandardItem(ia.getName()),
				QtGui.QStandardItem(ia.getRole()),
				QtGui.QStandardItem(ia.getBu())]
			self.IAs_model.appendRow(r)

	def on_addNew_ING(self):
		self.add_ING_Diag = Diag_addING_Window(MainWindow.__PATH_ADDING_UI, self.database)
		if self.add_ING_Diag.userInputCheck:
			self.INGs_model.appendRow(QtGui.QStandardItem(self.add_ING_Diag.userNameText))
		self.update_business_ing_table()

	def on_edit_ing(self):
		self.edit_ing_Diag = Diag_editING_Window(MainWindow.__PATH_EDITING_UI, self.ingSelected[0].data(), self.database)
		self.update_business_ing_table()

	def on_remove_Ing(self):
		res = Diag_delete_ing_ia(MainWindow.__PATH_DELUSER_UI, User._ING, self.ingSelected[0].data(), self.database)
		if (res.deleted):
			self.INGs_model.removeRow(self.ingSelected[0].row())
		self.update_business_ing_table()
		if self.INGs_model.rowCount() == 0:
			self.remove_ING.setEnabled(False)

	def on_remove_IA(self):
		res = Diag_delete_ing_ia(MainWindow.__PATH_DELUSER_UI, User._IA, self.iaSelected[0].data(), self.database)
		if (res.deleted):
			self.IAs_model.removeRow(self.iaSelected[0].row())
		if self.IAs_model.rowCount() == 0:
			self.remove_IA.setEnabled(False)
	def on_remove_BU(self):
		content = self.database.getContent()
		buText = self.buSelected[0].data()
		if buText != None:
			for nIa in content["BUs"][buText]["IAs"]:
				ia = IngAffaire.load(self.database, nIa)
				if ia != None:
					ia.removeFromBu(buText)
					ia.save()
				else:
					print ("error - remove BU - ia {} not found".format(nIa))
			for nIng in content["BUs"][buText]["INGs"]:
				ing = ING.load(self.database, nIng)
				if ing != None:
					ing.removeFromBu(buText)
					ing.save()
				else:
					print ("error - remove BU - ing {} not found".format(nIa))
			del content["BUs"][buText]
			self.database.write(content)
			self.BUs_model.removeRow(self.buSelected[0].row())
			if len(content["BUs"]) == 0:
				self.addNew_IA.setEnabled(False)
				self.addNew_ING.setEnabled(False)
			self.business_BuSelector.setCurrentIndex(0)


	def update_activity_tableView(self, data, IA_name, week_year):
		# get IA's ID from his name
		ia = IngAffaire.load(self.database, self.selectedIA)
		activities = ia.getActivitiesFromWeek(str(self.currentWeek[0])+"_"+str(self.currentWeek[1]))
		for i in range(self.activity_model.columnCount()):
			item =  QtGui.QStandardItem(str(activities[i]))
			item.setTextAlignment(QtCore.Qt.AlignCenter)
			self.activity_model.setItem(0, i, item)
		self.activity_list.setModel(self.activity_model)

	def on_Ings_list_selected(self):
		self.ingSelected = self.INGs_list.selectionModel().selectedRows()
		self.remove_ING.setEnabled(True)
		self.edit_ING.setEnabled(True)

	def on_IAs_list_selected(self):
		self.iaSelected = self.IAs_list.selectionModel().selectedRows()
		self.remove_IA.setEnabled(True)

	def on_BUs_list_selected(self):
		self.buSelected = self.Bus_list.selectionModel().selectedRows()
		self.remove_BU.setEnabled(True)

	def on_activity_IAselected(self):
		self.selectedIA = self.activity_IAs_list.currentIndex().data()
		if self.currentWeek != None:
			self.update_activity_tableView(self.database, self.selectedIA, self.currentWeek)
		ia = IngAffaire.load(self.database, self.selectedIA)
		self._activity_update_metrics(ia)

	def on_calendar_select(self):
		selectedDay = self.activity_calendar.selectedDate()
		self.currentWeek = selectedDay.weekNumber()
		if self.selectedIA != None:
			self.update_activity_tableView(self.database, self.selectedIA, self.currentWeek)

	def update_activity_IAMGR_list(self):
		content = self.database.getContent()
		selectedBU = self.activity_detailBU_selector.currentText()
		if selectedBU == '' or selectedBU == None or selectedBU == "None":
			self.activity_manager_selector.clear()
			return
		self.activity_IAMGR_list_model = QtGui.QStandardItemModel()
		for iaInBu in content["BUs"][selectedBU]["IAs"]:
			ia = IngAffaire.load(self.database, iaInBu)
			if (ia.isManagerIA()):
				self.activity_IAMGR_list_model.appendRow(QtGui.QStandardItem(iaInBu))
		self.activity_manager_selector.setModel(self.activity_IAMGR_list_model)
		self.update_activity_IA_list()

	def update_activity_IA_list(self):
		self.activity_IAs_list_model = QtGui.QStandardItemModel()
		self.activity_IAs_list.setModel(self.activity_IAs_list_model)
		self.activity_IAs_list_model.setColumnCount(1)
		self.activity_IAs_list_model.setHeaderData(0, QtCore.Qt.Horizontal, "Name")

		content = self.database.getContent()
		#get current selected BU
		selectedBU = self.activity_detailBU_selector.currentText()
		if selectedBU == '' or selectedBU == None or selectedBU == "None":
			self.activity_IAs_list_model.clear()
			return
		selectedMGR = self.activity_manager_selector.currentText()
		if selectedMGR == '' or selectedMGR == None or selectedMGR == "None":
			# if no manager in BU display all ia
			self.activity_IAs_list_model.clear()
			for iaInBu in content["BUs"][selectedBU]["IAs"]:
				ia = IngAffaire.load(self.database, iaInBu)
				self.activity_IAs_list_model.appendRow(QtGui.QStandardItem(iaInBu))
			return
		for iaInBu in content["BUs"][selectedBU]["IAs"]:
			ia = IngAffaire.load(self.database, iaInBu)
			if ia.getManagerName() == selectedMGR:
				self.activity_IAs_list_model.appendRow(QtGui.QStandardItem(iaInBu))

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
			ia = IngAffaire.load(self.database, self.selectedIA)
			if ia == None:
				alert = QtWidgets.QMessageBox()
				alert.setText("error - " + self.selectedIA + "Not found in database...")
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
			ia.save()
			# update metrics
			self._activity_update_metrics(ia)

	def _activity_update_metrics(self, ia):
		res = ia.getTxTransfo()
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
		ing = ING.load(self.database, self.business_Ing_selected)
		if ing.getState() == ING.STATES[ING.ING_STATE_MI]:
			self.ingStopMission.setEnabled(True)
			self.ingStartMission.setEnabled(False)
		else:
			self.ingStartMission.setEnabled(True)
			self.ingStopMission.setEnabled(False)

	def update_business_ing_table(self):
		if self.business_ing_table_model != None:
			self.business_ing_table_model.clear()
		self.business_ing_table_model = self.init_business_table()
		self.populate_ing_business_ingIO()
		self.populate_ing_business_MissionIO()
		self.business_ing_table.setModel(self.business_ing_table_model)
		self.update_business_textLabel()


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
		content = self.database.getContent()
		currentBU = self.business_BuSelector.currentText()
		for ing in content["INGs"]:
			if any(bu == currentBU for bu in content["INGs"][ing]["BU"]):
				entryDate = QtCore.QDate.fromString(content['INGs'][ing]['entryDate'], "dd.MM.yyyy")
				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = str(entryDate.weekNumber()[1])
				for i in range(self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr: #and currentYear == entryDateYearNbr:
						self._add_ing_enter_ingIO(content["INGs"][ing], i)


		for ing in content['archive']["INGs"]:
			if any(bu == currentBU for bu in content['archive']["INGs"][ing]["BU"]):
				entryDate = QtCore.QDate.fromString(content['archive']["INGs"][ing]['entryDate'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content['archive']["INGs"][ing]['exitDate'], "dd.MM.yyyy")
				exitDateWeekNbr = str(exitDate.weekNumber()[0])
				exitDateYearNbr = str(exitDate.weekNumber()[1])
				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = str(entryDate.weekNumber()[1])
				for i in range(self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr: #and currentYear == entryDateYearNbr:
						self._add_ing_enter_ingIO(content['archive']["INGs"][ing], i)
					if currentRowVerticalHeader == exitDateYearNbr+":"+exitDateWeekNbr: # and currentYear == exitDateYearNbr:
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
			totalNewIng = cellContent.text().count(',') + 1
			self.business_ing_table_model.setItem(rowIndex, 7,  QtGui.QStandardItem(str(totalNewIng)))

	def populate_ing_business_MissionIO(self, ing_id=None):
		content = self.database.getContent()
		currentBU = self.business_BuSelector.currentText()

		for ing in content["INGs"]:
			if any(bu == currentBU for bu in content["INGs"][ing]["BU"]):

				if not 'mission_Start' in content["INGs"][ing].keys() and not 'mission_Stop' in content["INGs"][ing].keys():
					continue
				entryDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Start'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content['INGs'][ing]['mission_Stop'], "dd.MM.yyyy")

				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = str(entryDate.weekNumber()[1])
				exitDateWeekNbr = str(exitDate.weekNumber()[0])
				exitDateYearNbr = str(exitDate.weekNumber()[1])

				for i in range (self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					# draw current
					if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr:
						self._add_ing_start_mission(content["INGs"][ing], i)
					if  currentRowVerticalHeader == exitDateYearNbr+":"+exitDateWeekNbr:
						self._add_ing_stop_mission(content["INGs"][ing], i)
					# draw passed:
					for pMission in content["INGs"][ing]["prev_mission"]:
						entryDate = QtCore.QDate.fromString(content['INGs'][ing]["prev_mission"][pMission]['mission_Start'], "dd.MM.yyyy")
						exitDate = QtCore.QDate.fromString(content['INGs'][ing]["prev_mission"][pMission]['mission_Stop'], "dd.MM.yyyy")

						entryDateWeekNbr = str(entryDate.weekNumber()[0])
						entryDateYearNbr = str(entryDate.weekNumber()[1])
						exitDateWeekNbr = str(exitDate.weekNumber()[0])
						exitDateYearNbr = str(exitDate.weekNumber()[1])
						if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr:
							self._add_ing_start_mission(content["INGs"][ing], i)
							self._add_ing_stop_mission(content["INGs"][ing], i)


		for ing in content["archive"]["INGs"]:
			if any(bu == currentBU for bu in content["archive"]["INGs"][ing]["BU"]):

				if not 'mission_Start' in content["archive"]["INGs"][ing].keys() and not 'mission_Stop' in content["archive"]["INGs"][ing].keys():
					continue
				entryDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]['mission_Start'], "dd.MM.yyyy")
				exitDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]['mission_Stop'], "dd.MM.yyyy")

				entryDateWeekNbr = str(entryDate.weekNumber()[0])
				entryDateYearNbr = str(entryDate.weekNumber()[1])
				exitDateWeekNbr = str(exitDate.weekNumber()[0])
				exitDateYearNbr = str(exitDate.weekNumber()[1])

				for i in range (self.business_ing_table_model.rowCount()):
					currentRowVerticalHeader = self.business_ing_table_model.verticalHeaderItem(i).text()
					# draw current
					if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr:
						self._add_ing_start_mission(content["archive"]["INGs"][ing], i)
					if  currentRowVerticalHeader == exitDateYearNbr+":"+exitDateWeekNbr:
						self._add_ing_stop_mission(content["archive"]["INGs"][ing], i)
					# draw passed:
					for pMission in content["archive"]["INGs"][ing]["prev_mission"]:
						entryDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]["prev_mission"][pMission]['mission_Start'], "dd.MM.yyyy")
						exitDate = QtCore.QDate.fromString(content["archive"]['INGs'][ing]["prev_mission"][pMission]['mission_Stop'], "dd.MM.yyyy")

						entryDateWeekNbr = str(entryDate.weekNumber()[0])
						entryDateYearNbr = str(entryDate.weekNumber()[1])
						exitDateWeekNbr = str(exitDate.weekNumber()[0])
						exitDateYearNbr = str(exitDate.weekNumber()[1])
						if currentRowVerticalHeader == entryDateYearNbr+":"+entryDateWeekNbr:
							self._add_ing_start_mission(content["archive"]["INGs"][ing], i)
							self._add_ing_stop_mission(content["archive"]["INGs"][ing], i)


	def on_business_ingStartMission(self):
		self.diag_business_startMission = Diag_business_ING_startMission(MainWindow.__PATH_STARTMISSION_UI, self.business_Ing_selected, self.database)
		self.update_business_ing_table()

	def on_business_ingStopMission(self):
		self.diag_business_stopMission = Diag_business_ING_stopMission(MainWindow.__PATH_STOPMISSION_UI, self.business_Ing_selected, self.database)
		self.update_business_ing_table()

	def on_business_manager_selected(self):
		self.business_Ing_list_model = QtGui.QStandardItemModel()
		self.business_Ing_list_model.setColumnCount(1)
		self.business_Ing_list_model.setHeaderData(0, QtCore.Qt.Horizontal, "Ings-Name")
		self.business_Ing_list.setModel(self.business_Ing_list_model)
		content = self.database.getContent()
		selectedBU = self.business_BuSelector.currentText()
		if selectedBU == "" or selectedBU == None:
			return
		selectedMGR = self.business_managerSelector.currentText()
		# if no manager in Bu display all ing
		if selectedMGR == '' or selectedMGR == None or selectedMGR == "None":
			self.business_Ing_list_model.clear()
			for ingInBu in content["BUs"][selectedBU]["INGs"]:
				ing = ING.load(self.database, ingInBu)
				self.business_Ing_list_model.appendRow(QtGui.QStandardItem(ingInBu))
		else:
			for ingInBu in content["BUs"][selectedBU]["INGs"]:
				ing = ING.load(self.database, ingInBu)
				if ing.getManagerName() == selectedMGR:
					self.business_Ing_list_model.appendRow(QtGui.QStandardItem(ingInBu))
		self.update_business_ing_table()

	def on_business_BU_selected(self):
		content = self.database.getContent()
		selectedBU = self.business_BuSelector.currentText()
		if selectedBU == "" or selectedBU == None:
			self.business_managerSelector.clear()
			return
		self.business_manager_list_model = QtGui.QStandardItemModel()
		for iaInBu in content["BUs"][selectedBU]["IAs"]:
			ia = IngAffaire.load(self.database, iaInBu)
			if (ia.isManagerING()):
				self.business_manager_list_model.appendRow(QtGui.QStandardItem(iaInBu))
		self.business_managerSelector.setModel(self.business_manager_list_model)
		self.on_business_manager_selected()

	def util_getWeeknumbers(self):
		self.business_current_date = self.business_current_date_selector.date()
		verticalHeaderLabels = []
		currentMonth = QtCore.QDate(self.business_current_date.year(), self.business_current_date.month(), 1)
		prevMonth = currentMonth.addMonths(-1)
		nextMonth = currentMonth.addMonths(2)
		currentMonth = prevMonth
		while currentMonth.daysTo(nextMonth) >= 0:
			verticalHeaderLabels.append(str(currentMonth.weekNumber()[1])+":"+str(currentMonth.weekNumber()[0]))
			currentMonth = currentMonth.addDays(7)
		return verticalHeaderLabels

	def on_business_date_changed(self):
		if self.business_ing_table_model != None:
			self.business_ing_table_model.clear()
		self.business_ing_table_model = self.init_business_table()
		# populate table
		self.populate_ing_business_MissionIO()
		self.populate_ing_business_ingIO()

	def update_business_textLabel(self):
		content = self.database.getContent()
		curBu = self.business_BuSelector.currentText()
		if curBu == '' or curBu == None:
			self.business_tot_IngInBU.setText("/")
			self.business_tot_IngInMission.setText("/")
			self.business_tot_IngActivityRatio.setText("/")
			return
		ingInBu = len(content["BUs"][curBu]["INGs"])
		ingInMission = 0
		for ing in content["BUs"][curBu]["INGs"]:
			ing = ING.load(self.database, ing)
			if ing.getState() == ING.STATES[ING.ING_STATE_MI]:
				ingInMission += 1
		if ingInBu != 0:
			rate = ingInMission / ingInBu * 100
		else:
			rate = 0
		self.business_tot_IngInBU.setText(str(ingInBu))
		self.business_tot_IngInMission.setText(str(ingInMission))
		self.business_tot_IngActivityRatio.setText(str(rate)+"%")

	def verifyData(self):
		pass
		# content = self.database.getContent()
		# warningIngNames_reset = []
		# warningIngNames_3days = []
		# for ing in content["INGs"]:
		# 	ingName = content["INGs"][ing]["name"]
		# 	#mission_Start = QtCore.QDate().fromString(content["INGs"][ing]['mission_Start'], "dd.MM.yyyy")
		# 	mission_Stop = QtCore.QDate().fromString(content["INGs"][ing]['mission_Stop'], "dd.MM.yyyy")
		# 	#currentState = content["INGs"][ing]['state']
		# 	if self.today.daysTo(mission_Stop) < 3:
		# 		warningIngNames_3days.append(ingName)
		# 	if self.today.daysTo(mission_Stop) <= 0:
		# 		content["INGs"][ing]["state"] = "without Mission"
		# 		content["INGs"][ing]["current_client"] = ""
		# 		warningIngNames_reset.append(ingName)

		# N = len(warningIngNames_3days)
		# if N > 0:
		# 	message = "Warning - ["
		# 	for i, name in enumerate(warningIngNames_3days):
		# 		message += name
		# 		if i < N - 1:
		# 			message += ', '
		# 	message += '] will stop their mission in less than 3 day !'
		# 	alert = QtWidgets.QMessageBox()
		# 	alert.setText(message)
		# 	alert.exec_()

		# N = len(warningIngNames_reset)
		# if N > 0:
		# 	message = "Warning - Automatic Reset for : ["
		# 	for i, name in enumerate(warningIngNames_3days):
		# 		message += name
		# 		if i < N - 1:
		# 			message += ', '
		# 	message += ']'
		# 	alert = QtWidgets.QMessageBox()
		# 	alert.setText(message)
		# 	alert.exec_()


class businessIngListDelegate(QtWidgets.QItemDelegate):
	"""
	abstract class to render listed engineer name in the business tab
	"""
	def __init__(self, parent=None, *args):
		QtWidgets.QItemDelegate.__init__(self, parent, *args)
		self.database = parent.database

	def paint(self, painter, option, index):
		painter.save()
		ing = ING.load(self.database, index.data())
		if ing != None:
			if option.state & QtWidgets.QStyle.State_Selected:
				painter.setBrush(QtGui.QBrush(QtGui.QColor(QtCore.Qt.lightGray)))
				painter.drawRect(option.rect)
			today = QtCore.QDate.currentDate()
			if ing.getState() == ING.STATES[ING.ING_STATE_MI]:
				stopMissionDate = QtCore.QDate().fromString(ing.getMissionStop(), "dd.MM.yyyy")
				remains = today.daysTo(stopMissionDate)
				if remains > 3:
					painter.setPen(QtCore.Qt.darkGreen)
				elif remains <= 3:
					painter.setPen(QtCore.Qt.darkYellow)
			else:
				painter.setPen(QtCore.Qt.darkRed)
		painter.drawText(option.rect, QtCore.Qt.AlignCenter, index.data())
		painter.restore()