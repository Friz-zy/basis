#!/usr/bin/env python2
# coding=utf-8

import os
import sys
import codecs
import urllib2

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

		
		self.setWindowTitle(self.title)
		self.webView = QtWebKit.QWebView()
		self.webView.urlChanged.connect(self.beforeLoadPage)
		self.url = QtGui.QLineEdit()
		self.url.returnPressed.connect(self.urlChanged)
		self.setCentralWidget(self.webView)
		self.menubar = self.menuBar()
		self.toolbarMenu = self.addToolBar('Navigation')
		self.statusBar()
		
		self.printer = QtGui.QPrinter()

		# main menu & actions
		self.loadAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					  "document-open"),'&Open', self)
		self.loadAction.setShortcut('Ctrl+O')
		self.loadAction.setStatusTip('Openfile')
		self.loadAction.triggered.connect(self.open)

		self.saveAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					  "document-save"),'&Save', self)
		self.saveAction.setShortcut('Ctrl+S')
		self.saveAction.setStatusTip('Save file')
		self.saveAction.triggered.connect(self.save)

		self.saveAsAction = QtGui.QAction(QtGui.QIcon.fromTheme(
				    "document-save-as"),'&Save as', self)
		self.saveAction.setStatusTip('Save file as')
		self.saveAsAction.triggered.connect(self.saveAs)

		self.printItAction = QtGui.QAction(QtGui.QIcon.fromTheme(
						    ""),'&Print it', self)
		self.printItAction.setStatusTip('Print this page')
		self.printItAction.triggered.connect(self.printIt)

		self.aboutAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					    "help-about"),'&About', self)
		self.aboutAction.triggered.connect(self.about)

		self.quitAction = QtGui.QAction(QtGui.QIcon.fromTheme(
				      "application-exit"),'&Quit', self)
		self.quitAction.setShortcut('Ctrl+Q')
		self.quitAction.setStatusTip('Exit application')
		self.quitAction.triggered.connect(self.close)

		self.fileMenu = self.menubar.addMenu('&File')
		self.fileMenu.addAction(self.loadAction)
		self.fileMenu.addAction(self.saveAction)
		self.fileMenu.addAction(self.saveAsAction)
		self.fileMenu.addAction(self.printItAction)
		self.fileMenu.addAction(self.aboutAction)
		self.fileMenu.addAction(self.quitAction)

		# toolbar & actions
		self.backAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					    "go-previous"),'&Back', self)
		self.backAction.setStatusTip('Back')
		self.backAction.triggered.connect(self.back)
		self.toolbarMenu.addAction(self.backAction)

		self.forwardAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					      "go-next"),'&Forward', self)
		self.forwardAction.setStatusTip('Forward')
		self.forwardAction.triggered.connect(self.forward)
		self.toolbarMenu.addAction(self.forwardAction)

		self.stopAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					  "process-stop"),'&Stop', self)
		self.stopAction.setStatusTip('Stop')
		self.stopAction.triggered.connect(self.stop)
		self.toolbarMenu.addAction(self.stopAction)

		self.reloadAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					    "view-refresh"),'&Reload', self)
		self.reloadAction.setStatusTip('Reload')
		self.reloadAction.triggered.connect(self.reload)
		self.toolbarMenu.addAction(self.reloadAction)
		
		self.toolbarMenu.addWidget(self.url)
		
		self.runAction = QtGui.QAction(QtGui.QIcon.fromTheme(
					    "system-run"),'&Run', self)
		self.runAction.setStatusTip('Run')
		self.runAction.triggered.connect(self.urlChanged)
		self.toolbarMenu.addAction(self.runAction)

	def loadConfig(self):
		self.defaultSearche = "https://google.com/?q="
		self.homeDirectory = os.path.expanduser("~")
		self.title = 'Browser'

	def saveConfig(self):
		pass

	def open(self):
		self.webView.setUrl(QtCore.QUrl("file://" + \
		  self.showFileOpenDialog(self.homeDirectory)[0]))

	def save(self):
		title = self.webView.title()
		if title == "":
			title = self.url.text()
		if ".html" not in title and title != "": title += ".html"
		if title != "":
			filename = os.path.join(self.homeDirectory, title)
			self.saveHtml(filename)

	def saveAs(self):
		title = self.webView.title()
		if title == "":
			title = self.url.text()
		if ".html" not in title and title != "": title += ".html"
		filename = self.showFileSaveDialog(title,
				     self.homeDirectory)[0]
		self.saveHtml(filename)

	def saveHtml(self, filename):
		if filename is not None:
			if ".html" not in filename: filename += ".html"
			#filename.replace(" ", "+")
			data = self.webView.page().mainFrame().toHtml()
			with codecs.open(filename, encoding="utf-8",
							mode="w") as f:
				f.write(data)

	def printIt(self):
		if QtGui.QPrintDialog(self.printer,
			      self).exec_() == QtGui.QDialog.Accepted:
			self.webView.print_(self.printer)

	def about(self):
		about = ""
		self.showMessage("About", about)

	def back(self):
		self.webView.back()

	def forward(self):
		self.webView.forward()

	def stop(self):
		self.webView.stop()

	def reload(self):
		self.webView.reload()

	def urlChanged(self):
		text = self.url.text()
		pattern = "://"
		if " " in text:
			if " " == text[0] or " " != text[-1]:
				if pattern in text:
					begin_url = text.find(pattern)
					end_url = text.find(" ", begin_url)
					url = text[begin_url+len(pattern):end_url]
					search = text - url
					text = self.defaultSearche + search + "+site%3" + url
				else:
					text = self.defaultSearche + text
				text.replace(" ", "+")
		else:
			if pattern in text:
				if not self.checkUrlGood(text):
					text = self.defaultSearche + text
			else:
				if not self.checkUrlGood("https://" + text):
					if not self.checkUrlGood("http://" + text):
						text = self.defaultSearche + text
					else:
						  text = "http://" + text
				else:
					text = "https://" + text
		self.webView.setUrl(QtCore.QUrl(text))
		if self.webView.title() != "":
			self.setWindowTitle(self.webView.title() + " - " + self.title)

	def beforeLoadPage(self, url):
		self.url.setText(url.toString())

	def checkUrlGood(self, url):
		try:
			urllib2.urlopen(urllib2.Request(str(url)))
			return True
		except:
			return False	

	def showFileOpenDialog(self, path='.', filer=""):
		return QtGui.QFileDialog.getOpenFileName(self,
				      'Open file', path, filer)

	def showFileSaveDialog(self, path='.', filer=""):
		return QtGui.QFileDialog.getSaveFileName(self,
				    'Save file as:', path, filer)

	def showMessage(self, title, text):
		QtGui.QMessageBox.information(self, str(title), str(text))

	def showCritical(self, title, text):
		QtGui.QMessageBox.critical(self, str(title), str(text))

	def closeEvent(self, e):
		self.saveConfig()
		print "bye!"
		self.close()

if __name__ == "__main__":
	app = QtGui.QApplication(sys.argv)
	myapp = Main()
	myapp.show()
	sys.exit(app.exec_()) 
