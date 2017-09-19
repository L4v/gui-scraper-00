
import sys
import requests
from PyQt4 import QtCore, QtGui
from PyQt4.QtGui import QApplication, QMainWindow
from bs4 import BeautifulSoup as bs

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class Ui_MainWindow(object):

    checkState = False
    fileData = ""

    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(800, 600)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        # URL LINEEDIT
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(20, 30, 391, 29))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))

        # SCRAPE BUTTON
        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(420, 30, 101, 29))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton.clicked.connect(self.scrape)

        # EXPORT BUTTON
        self.exportButton = QtGui.QPushButton(self.centralwidget)
        self.exportButton.setGeometry(QtCore.QRect(666, 216, 101, 29))
        self.exportButton.setObjectName(_fromUtf8("exportButton"))
        self.exportButton.setEnabled(self.checkState)
        self.exportButton.clicked.connect(self.export_file)

        self.frame = QtGui.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(20, 80, 501, 471))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.textEdit = QtGui.QTextEdit(self.frame)
        self.textEdit.setGeometry(QtCore.QRect(10, 50, 481, 411))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(27, 9, 461, 31))
        self.label.setStyleSheet(_fromUtf8(""))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))

        # TAG
        self.lineEdit_2 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_2.setGeometry(QtCore.QRect(540, 110, 71, 29))
        self.lineEdit_2.setObjectName(_fromUtf8("lineEdit_2"))

        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(542, 90, 68, 17))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(655, 90, 101, 17))
        self.label_3.setObjectName(_fromUtf8("label_3"))

        self.lineEdit_3 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_3.setGeometry(QtCore.QRect(650, 110, 113, 29))
        self.lineEdit_3.setObjectName(_fromUtf8("lineEdit_3"))

        # EXPORT CHECKBOX
        self.checkBox = QtGui.QCheckBox(self.centralwidget)
        self.checkBox.setGeometry(QtCore.QRect(540, 220, 121, 22))
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkBox.clicked.connect(self.check_export)

        # EXPORT LINEEDIT
        self.lineEdit_4 = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit_4.setGeometry(QtCore.QRect(540, 180, 241, 29))
        self.lineEdit_4.setObjectName(_fromUtf8("lineEdit_4"))
        self.lineEdit_4.setEnabled(self.checkState)

        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(540, 160, 68, 17))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 23))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "Enter URL to scrape from", None))
        self.pushButton.setText(_translate("MainWindow", "Scrape", None))
        self.exportButton.setText(_translate("MainWindow", "Export", None))
        self.label.setText(_translate("MainWindow", "PREVIEW", None))
        self.lineEdit_2.setToolTip(_translate("MainWindow", "Enter desired tag for scraping", None))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "Tag", None))
        self.label_2.setText(_translate("MainWindow", "Tag name", None))
        self.label_3.setText(_translate("MainWindow", "Class(optional)", None))
        self.lineEdit_3.setToolTip(_translate("MainWindow", "Leave blank if none", None))
        self.lineEdit_3.setPlaceholderText(_translate("MainWindow", "Class", None))
        self.checkBox.setText(_translate("MainWindow", "Export to file", None))
        self.lineEdit_4.setToolTip(_translate("MainWindow", "Name of exported file", None))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "Name of file", None))
        self.label_4.setText(_translate("MainWindow", "Filename:", None))

    # SCRAPE FUNCTION
    def scrape(self):
        url = self.lineEdit.text()
        tag = self.lineEdit_2.text()
        tag_class = self.lineEdit_3.text()
        r = requests.get("http://" + url)
        data = r.text
        soup = bs(data, "html.parser")

        self.textEdit.clear()
        if(self.lineEdit_3.text().isEmpty()):
            for link in soup.findAll(tag):
                linkText = unicode(link).encode('utf-8')
                self.textEdit.append(linkText)
        else:
            for link in soup.findAll(tag, {"class": tag_class}):
                linkText = unicode(link).encode('utf-8')
                self.textEdit.append(linkText)

    # SWITCH EXPORT ON/OFF
    def check_export(self):
        self.checkState = not self.checkState
        self.lineEdit_4.setEnabled(self.checkState)
        self.exportButton.setEnabled(self.checkState)

    # EXPORT FILE FUNCTION
    def export_file(self):
        fileName = self.lineEdit_4.text()
        fileData = self.textEdit.toPlainText()
        f = open(fileName, 'w')

        f.write(fileData)
        f.close()


# MAIN CALL
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(window)

    window.show()
    sys.exit(app.exec_())
