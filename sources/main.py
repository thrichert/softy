from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore, QtGui
import sys, os, json

class DB(object):
	def __init__(self, path):
		self.path = path
		if not os.path.exists(path):
			print('create DB')
			self.data = {
				"IAs":[],
				"INGs":[]
			}
			with open(path, 'w') as f:
				f.write(json.dumps(self.data, sort_keys=True, indent=4))
		else:
			print('read DB')
			with open(path, 'r') as f:
				self.data = json.load(f)

	def write(self, data):
		self.data = data
		with open(self.path, 'w+') as f:
			f.write(json.dumps(self.data, sort_keys=True, indent=4))

	def getContent(self):
		return self.data

class MainWindow(QtWidgets.QMainWindow):
	def __init__(self):
		super(MainWindow, self).__init__()
		uic.loadUi("./sources/views/mainWindow.ui", self)
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
		self.add_IA_Diag = Diag_addIA_Window("./sources/views/add_IA_Diag.ui")

	def on_addNew_ING(self):
		self.add_ING_Diag = Diag_addING_Window("./sources/views/add_ING_Diag.ui")

	def update_IA_tableView(self, data):
		# get info from DB
		self.IAs_list = self.findChild(QtWidgets.QTableView, "IAsList")
		self.IAs_list.setModel(self.IAs_model)
		for colID, IA in enumerate(data["IAs"]):
			name = QtGui.QStandardItem(IA["name"])
			role = QtGui.QStandardItem(IA["role"])
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
			name = QtGui.QStandardItem(ING["name"])
			name.setFlags(QtCore.Qt.NoItemFlags)
			self.INGs_model.setItem(colID, 0, name)

	def update_activity_tableView(self, data, user, week):
		self.activity_list = self.findChild(QtWidgets.QTableView, "activityList")
		self.activity_list.setModel(self.activity_model)
		#get info from DB
		info = data[user]
		print(info)

	def on_activity_IAselected(self):
		self.selectedIA = self.activity_IAs_list.currentIndex().data()
		if self.currentWeek != None:
			self.update_activity_tableView(database.getContent(), self.selectedIA, self.currentWeek)

	def update_activity_IA_list(self, data):
		#get info from DB
		self.activity_IAs_list = self.findChild(QtWidgets.QListView, "Activity_IAsList")
		model = QtGui.QStandardItemModel()
		self.activity_IAs_list.setModel(model)
		for ia in data["IAs"]:
			model.appendRow(QtGui.QStandardItem(ia["name"]))

	def on_activity_table_dataChange(self, index):
		print('data changed in activity table')
		# check user input
		userInput = self.activity_model.itemFromIndex(index)
		if not userInput.text().isnumeric():
			userInput.clearData()
			alert = QtWidgets.QMessageBox()
			alert.setText("error - Input can only be numbers")
			alert.exec_()
		else:
			# save data
			data = database.getContent()

			data[self.selectedIA][str(self.currentWeek[0])+"_"+str(self.currentWeek[1])] = {"test":userInput}
			#database.write(data)

	def on_calendar_select(self):
		selectedDay = self.activity_calendar.selectedDate()
		self.currentWeek = selectedDay.weekNumber()
		if self.selectedIA != None:
			self.update_activity_tableView(database.getContent(), self.selectedIA, self.currentWeek)

class Diag_addIA_Window(QtWidgets.QDialog):
	def __init__(self, viewPath):
		super(Diag_addIA_Window, self).__init__()
		uic.loadUi(viewPath,self)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			#check user input
			userName = self.findChild(QtWidgets.QLineEdit, "IA_Name")
			userRole = self.findChild(QtWidgets.QComboBox, "IA_Role")
			if userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				newUser = {"name" : userName.text(), "role" : userRole.currentText()}
				print ("New IA added")

				data = database.getContent()
				# add to IA's list
				data["IAs"].append(newUser)
				# create specific dictionary for this IA
				data[userName.text()] = {}
				database.write(data)
				#update QlistView in mainWindow
				mainWindow.update_IA_tableView(data)
		else:
			print('Nop')

class Diag_addING_Window(QtWidgets.QDialog):
	def __init__(self, viewPath):
		super(Diag_addING_Window, self).__init__()
		uic.loadUi(viewPath,self)
		resp = self.exec_()
		if resp == QtWidgets.QDialog.Accepted:
			#check user input
			userName = self.findChild(QtWidgets.QLineEdit, "ING_Name")
			if userName.text() == "":
				alert = QtWidgets.QMessageBox()
				alert.setText("error - UserName cannot be empty")
				alert.exec_()
			else:
				#add new IA to db
				newUser = {"name" : userName.text()}
				print ("New ING added")
				data = database.getContent()
				data["INGs"].append(newUser)
				database.write(data)
				#update QlistView in mainWindow
				mainWindow.update_ING_tableView(data)
		else:
			print('Nop')


if __name__ == "__main__":
	# init DB
	database = DB("./DataBase/db.json")


	app = QtWidgets.QApplication(sys.argv)
	mainWindow = MainWindow()
	app.exec_()