# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainWindowPoAmsK.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import subprocess
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Main Window")
        Dialog.resize(907, 523)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, -20, 951, 561))
        font = QFont()
        font.setFamilies([u"Tw Cen MT Condensed"])
        font.setPointSize(16)
        font.setBold(False)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")
        self.label.setPixmap(QPixmap(u"images/resized.jpg"))
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 390, 231, 41))
        font1 = QFont()
        font1.setFamilies([u"Tw Cen MT Condensed Extra Bold"])
        font1.setPointSize(20)
        self.pushButton.setFont(font1)
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 0, 72);\n"
"}\n"   
"")
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(590, 220, 241, 41))
        self.pushButton_2.setFont(font1)
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 0, 72);\n"
"}\n"
"")
        self.pushButton_3 = QPushButton(Dialog)
        self.pushButton_3.clicked.connect(lambda: self.run_quick_scan(Dialog))
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setGeometry(QRect(320, 280, 241, 41))
        self.pushButton_3.setFont(font1)
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 0, 72);\n"
"}\n"
"")

        self.pushButton_4 = QPushButton(Dialog)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.clicked.connect(lambda: self.run_ram_booster(Dialog))
        self.pushButton_4.setGeometry(QRect(600, 330, 201, 41))
        self.pushButton_4.setFont(font1)
        self.pushButton_4.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(0, 0, 72);\n"
"}\n"
"")
        self.pushButton_5 = QPushButton(Dialog)
        self.pushButton_5.setObjectName(u"pushButton_5")
        self.pushButton_5.setGeometry(QRect(54, 133, 111, 31))
        font2 = QFont()
        font2.setFamilies([u"Tw Cen MT Condensed"])
        font2.setPointSize(14)
        self.pushButton_5.setFont(font2)
        self.pushButton_5.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")
        self.pushButton_6 = QPushButton(Dialog)
        self.pushButton_6.setObjectName(u"pushButton_6")
        self.pushButton_6.setGeometry(QRect(230, 133, 121, 31))
        font3 = QFont()
        font3.setFamilies([u"Tw Cen MT Condensed"])
        font3.setPointSize(16)
        self.pushButton_6.setFont(font3)
        self.pushButton_6.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")
        self.pushButton_7 = QPushButton(Dialog)
        self.pushButton_7.setObjectName(u"pushButton_7")
        self.pushButton_7.setGeometry(QRect(420, 133, 101, 31))
        self.pushButton_7.setFont(font3)
        self.pushButton_7.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")
        self.pushButton_8 = QPushButton(Dialog)
        self.pushButton_8.setObjectName(u"pushButton_8")
        self.pushButton_8.setGeometry(QRect(610, 133, 101, 31))
        font4 = QFont()
        font4.setFamilies([u"Tw Cen MT Condensed"])
        font4.setPointSize(16)
        font4.setBold(True)
        self.pushButton_8.setFont(font4)
        self.pushButton_8.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")
        self.pushButton_9 = QPushButton(Dialog)
        self.pushButton_9.setObjectName(u"pushButton_9")
        self.pushButton_9.setGeometry(QRect(780, 133, 111, 31))
        self.pushButton_9.setFont(font3)
        self.pushButton_9.setStyleSheet(u"QPushButton {\n"
"    background-color: rgb(49, 53, 98);\n"
"}\n"
"")

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)


    
    def run_quick_scan(self,Dialog):
        subprocess.Popen(['python', 'quickScanWindow.py'])
        Dialog.close()
        
    def run_ram_booster(self,Dialog):
        subprocess.Popen(['python', 'boosting_ram.py'])
        Dialog.close()

    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"CoreZ Advance Security", None))
        self.label.setText("")
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Full Scan", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Junk Cleaner", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", u"Quick Scan", None))
        
        self.pushButton_4.setText(QCoreApplication.translate("Dialog", u"RAM Booster", None))
        self.pushButton_5.setText(QCoreApplication.translate("Dialog", u"Dashboard", None))
        self.pushButton_6.setText(QCoreApplication.translate("Dialog", u"ULTRON", None))
        self.pushButton_7.setText(QCoreApplication.translate("Dialog", u"Settings", None))
        self.pushButton_8.setText(QCoreApplication.translate("Dialog", u"Privacy", None))
        self.pushButton_9.setText(QCoreApplication.translate("Dialog", u"Support", None))
    # retranslateUi



import sys
from PySide6.QtWidgets import QApplication, QDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of the dialog
    dialog = QDialog()

    # Create an instance of the Ui_Dialog class
    ui = Ui_Dialog()

    # Set up the user interface
    ui.setupUi(dialog)

    # Show the dialog
    dialog.show()

    # Execute the application
    sys.exit(app.exec())