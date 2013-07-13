#!/usr/bin/env python2
# coding=utf-8

import sys
try:
  from PySide import QtCore, QtGui, QtWebKit, QtNetwork
except:
	try:
		from PyQT import QtCore, QtGui, QtWebKit, QtNetwork
	except:
		print >> sys.stderr, "Error: can't load PySide or PyQT"
		sys.exit()

class Main(QtGui.QMainWindow):
  def __init__(self, parent=None):
		QtGui.QMainWindow.__init__(self, parent)

		self.loadConfig()

		# set size and background
		#self.setFixedSize(600, 400)
		#randImage = random.choice(getFiles("./images"))
		#if randImage:
		#	br = QtGui.QBrush()
		#	Image = QtGui.QImage(randImage)
		#	br.setTextureImage(Image.scaled(600, 400))
		#	plt = self.palette()
		#	plt.setBrush(plt.Background, br)
		#	self.setPalette(plt)
		#self.setWindowIcon(QtGui.QIcon(''))
		
		self.setWindowTitle('Main')
		self.webView = QtWebKit.QWebView()
		self.new()
		self.setCentralWidget(self.webView)
		self.menubar = self.menuBar()
		self.toolbarMenu = self.addToolBar('New')
		self.statusBar()

		# main actions
		self.createNewAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-new"),'&Create new', self)
		self.createNewAction.setStatusTip('Create new file')
		self.createNewAction.triggered.connect(self.new)
		
		self.loadAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-open"),'&Load', self)
		self.loadAction.setShortcut('Ctrl+O')
		self.loadAction.setStatusTip('Openfile')
		self.loadAction.triggered.connect(self.load)
		
		self.saveAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-save"),'&Save', self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip('Save file')
		self.saveAction.triggered.connect(self.save)
		
		self.saveAsAction = QtGui.QAction(QtGui.QIcon.fromTheme("document-save-as"),'&Save as', self)
		self.saveAsAction.triggered.connect(self.saveAs)
		
		self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme("help-about"),'&About', self)
		self.aboutAction.triggered.connect(self.about)
		
		self.quitAction = QtGui.QAction(QtGui.QIcon.fromTheme("application-exit"),'&Quit', self)
		self.quitAction.setShortcut('Ctrl+Q')
		self.quitAction.setStatusTip('Exit application')
		self.quitAction.triggered.connect(self.close)

		# main menu & toolbar
		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(self.createNewAction)
		self.fileMenu.addAction(self.loadAction)
		self.fileMenu.addAction(self.saveAction)
		self.fileMenu.addAction(self.saveAsAction)
		self.fileMenu.addAction(self.aboutAction)
		self.fileMenu.addAction(self.quitAction)

		self.toolbarMenu.addAction(self.createNewAction)
		self.toolbarMenu.addAction(self.loadAction)
		self.toolbarMenu.addAction(self.saveAction)
		self.toolbarMenu.addSeparator ()

		self.undoAction = QtGui.QAction(QtGui.QIcon.fromTheme("edit-undo"),'&Undo', self)
		self.undoAction.setStatusTip('Undo')
		self.undoAction.triggered.connect(self.undo)
		self.toolbarMenu.addAction(self.undoAction)

		self.redoAction = QtGui.QAction(QtGui.QIcon.fromTheme("edit-redo"),'&Redo', self)
		self.redoAction.setStatusTip('Redo')
		self.redoAction.triggered.connect(self.redo)
		self.toolbarMenu.addAction(self.redoAction)
		self.toolbarMenu.addSeparator ()

		# tray
		self.trayIconMenu = QtGui.QMenu(self)
		self.trayIconMenu.addAction(self.createNewAction)
		self.trayIconMenu.addAction(self.loadAction)
		self.trayIconMenu.addAction(self.saveAction)
		self.trayIconMenu.addAction(self.saveAsAction)
		self.trayIconMenu.addAction(self.aboutAction)
		self.trayIconMenu.addAction(self.quitAction)
		self.trayIconPixmap = QtGui.QPixmap('icons/Main.png')
		self.trayIcon = QtGui.QSystemTrayIcon(self)
		self.trayIcon.setContextMenu(self.trayIconMenu)
		self.trayIcon.setIcon(QtGui.QIcon(self.trayIconPixmap))
		self.trayIcon.show()
		self.trayIcon.activated.connect(self.changeVisible)

	def loadConfig(self):
		pass

	def saveConfig(self):
		pass

	def new(self):
		self.webView.load(QtCore.QUrl(""))
		self.webView.page().setContentEditable(True)

	def load(self):
		pass

	def save(self):
		pass

	def saveAs(self):
		pass

	def about(self):
		about = ""
		self.showMessage("About WYSIWYG", about)

	def undo(self):
		pass

	def redo(self):
		pass

	def showFileOnenDialog(self):
	# QStringList 	getOpenFileNames ( QWidget * parent = 0, const QString & caption = QString(), const QString & dir = QString(), const QString & filter = QString(), QString * selectedFilter = 0, Options options = 0 )
		return QtGui.QFileDialog.getOpenFileName(self, 'Open file', '.')

	def showFileSaveDialog(self):
	# QString 	getSaveFileName ( QWidget * parent = 0, const QString & caption = QString(), const QString & dir = QString(), const QString & filter = QString(), QString * selectedFilter = 0, Options options = 0 )
		return QtGui.QFileDialog.getSaveFileName(self, 'Save file as:', '.')

	def showMessage(self, title, text):
		QtGui.QMessageBox.information(self, str(title), str(text))

	def showCritical(self, title, text):
		QtGui.QMessageBox.critical(self, str(title), str(text))

	def changeVisible(self,r):
		if r == QtGui.QSystemTrayIcon.Trigger:
			if self.isHidden():
				self.showNormal()
			else:
				self.hide()
	
	def changeEvent(self, e):
	# e.type(): 105 - hide, 99 - show
		# to tray
		if self.isMinimized():
			self.hide()
			e.ignore()

	def closeEvent(self, e):
		self.saveConfig()
		print "bye!"
		self.close()


if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = Main()
	myapp.show()
	sys.exit(app.exec_())
