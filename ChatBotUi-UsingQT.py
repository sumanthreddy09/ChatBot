# -*- coding: utf-8 -*-

"""
File : ChatBotUi
Description : Ui for the chatbot.
Author : Sumanth Kaliki <sumanth.reddy542@gmail.com>
Date : 27-04-2018
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PredictModel import response

class Ui_Form(object):
    def AddTextToListView(self, listItem):
        self.listWidget.addItem(listItem)

    def OnButtonClicked(self):
        text = self.lineEdit.text()
        item1 = QtWidgets.QListWidgetItem(text, self.listWidget)
        item1.setTextAlignment(QtCore.Qt.AlignRight)
        self.AddTextToListView(item1)
        responseText = response(text)
        item2 = QtWidgets.QListWidgetItem(responseText, self.listWidget)
        self.AddTextToListView(item2)

    def OnTrainButtonClicked(self):
        import TrainModel
        messageBox = QtWidgets.QMessageBox()
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.about(self.FormTest,  "ChatBot", "Trained With the latest Data Set Successfully.")



    def setupUi(self, Form):
        self.FormTest = Form
        Form.setObjectName("ChatBot")
        Form.resize(389, 290)
        self.gridLayout = QtWidgets.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.TrainButton = QtWidgets.QPushButton(Form)
        self.TrainButton.setObjectName("TrainButton")
        self.verticalLayout_2.addWidget(self.TrainButton)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(Form)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.listWidget.setFont(font)
        self.listWidget.setAlternatingRowColors(True)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)
        self.sendButton = QtWidgets.QPushButton(Form)
        self.sendButton.setObjectName("sendButton")
        self.horizontalLayout.addWidget(self.sendButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 0, 0, 1, 1)

        self.retranslateUi(Form)
        self.sendButton.clicked.connect(self.OnButtonClicked)
        self.sendButton.clicked.connect(self.lineEdit.clear)
        self.lineEdit.returnPressed.connect(self.sendButton.click)
        self.TrainButton.clicked.connect(self.OnTrainButtonClicked)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("ChatBot", "ChatBot"))
        self.TrainButton.setText(_translate("ChatBot", "Train Model"))
        self.sendButton.setText(_translate("ChatBot", "Send"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

