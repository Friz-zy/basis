#!/usr/bin/env python2
# coding=utf-8
"""
Copyright (c) by Filipp Kucheryavy aka Frizzy <filipp.s.frizzy@gmail.com>
All rights reserved.

Redistribution and use in source and binary forms, with or without modification, are permitted 
provided that the following conditions are met:

a. Redistributions of source code must retain the above copyright notice, this list of 
conditions and the following disclaimer. 

b. Redistributions in binary form must reproduce the above copyright notice, this list of 
conditions and the following disclaimer in the documentation and/or other materials provided 
with the distribution. 

c. Neither the name of the nor the names of its contributors may be used to endorse or promote 
products derived from this software without specific prior written permission. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS 
OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY 
AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE 
COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, 
EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF 
SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF 
ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import sys
try:
  from PySide import QtCore, QtGui, QtWebKit, QtNetwork
except:
	try:
		from PyQt4 import QtCore, QtGui, QtWebKit, QtNetwork
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
		self.createNewAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					"document-new"),'&Create new', self)
		self.createNewAction.setStatusTip('Create new file')
		self.createNewAction.triggered.connect(self.new)
		
		self.loadAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					    "document-open"),'&Load', self)
		self.loadAction.setShortcut('Ctrl+O')
		self.loadAction.setStatusTip('Openfile')
		self.loadAction.triggered.connect(self.load)
		
		self.saveAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					   "document-save"),'&Save', self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip('Save file')
		self.saveAction.triggered.connect(self.save)
		
		self.saveAsAction = QtGui.QAction(QtGui.QIcon.fromTheme(
				      "document-save-as"),'&Save as', self)
		self.saveAsAction.triggered.connect(self.saveAs)
		
		self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					      "help-about"),'&About', self)
		self.aboutAction.triggered.connect(self.about)
		
		self.quitAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					  "application-exit"),'&Quit', self)
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

		self.undoAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					      "edit-undo"),'&Undo', self)
		self.undoAction.setStatusTip('Undo')
		self.undoAction.triggered.connect(self.undo)
		self.toolbarMenu.addAction(self.undoAction)

		self.redoAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					      "edit-redo"),'&Redo', self)
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
		return QtGui.QFileDialog.getOpenFileName(self,
					      'Open file', '.')

	def showFileSaveDialog(self):
		return QtGui.QFileDialog.getSaveFileName(self, 
					  'Save file as:', '.')

	def showMessage(self, title, text):
		QtGui.QMessageBox.information(self, str(title),
						      str(text))

	def showCritical(self, title, text):
		QtGui.QMessageBox.critical(self, str(title),
						      str(text))

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
