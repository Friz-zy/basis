#!/usr/bin/env python
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
import six

try:
    from PySide import QtGui, QtCore
except:
    try:
        from PyQt4 import QtGui, QtCore
    except:
        six.print_(("Error: can't load PySide or PyQT"), file=sys.stderr, end="\n", sep=" ")
        sys.exit()
 
class Password(QtGui.QDialog):
    def __init__(self, title="Input Password", message="Input your password here", parent=None):
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle(title)
        self.label = QtGui.QLabel(message, self)
        self.checkBox = QtGui.QCheckBox("Hide password", self)
        self.checkBox.setCheckState(QtCore.Qt.Checked)
        self.checkBox.stateChanged.connect(self.setPasswordVisible)
        self.textEdit = QtGui.QLineEdit(self)
        self.textEdit.setEchoMode(self.textEdit.Password)
        self.buttonBox = QtGui.QDialogButtonBox(self)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.addWidget(self.checkBox)
        layout.addWidget(self.textEdit)
        layout.addWidget(self.buttonBox)

    def setPasswordVisible(self, e):
        if e:
            self.textEdit.setEchoMode(self.textEdit.Password)
        else:
            self.textEdit.setEchoMode(self.textEdit.Normal)

    def setLabel(self, text):
        self.label.setText(text)

    def getPassword(self):
        if self.textEdit.text():
            return (self.textEdit.text(), True)
        return ("", False)

def password():
    app = QtGui.QApplication(sys.argv)
    dlg = Password()
    dlg.exec_()
    six.print_((dlg.getPassword()), file=sys.stdout, end="\n", sep=" ")
