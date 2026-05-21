# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'quick scan windowgJjCyN.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import os
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QSizePolicy, QWidget)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Quick Scan!")
        Dialog.resize(827, 519)
        self.label = QLabel(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(-30, -10, 861, 551))
        self.label.setPixmap(QPixmap(os.path.join(SCRIPT_DIR, "images", "background.png")))
        self.label_2 = QLabel(Dialog)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(220, 120, 471, 61))
        font = QFont()
        font.setFamilies([u"Algerian"])
        font.setPointSize(48)
        self.label_2.setFont(font)
        self.label_2.setTextFormat(Qt.TextFormat.RichText)
        self.label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_2.setWordWrap(True)
        self.pushButton = QPushButton(Dialog)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(330, 280, 211, 51))
        font1 = QFont()
        font1.setFamilies([u"Tw Cen MT Condensed Extra Bold"])
        font1.setPointSize(20)
        self.pushButton.setFont(font1)
        self.pushButton_2 = QPushButton(Dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setGeometry(QRect(350, 400, 181, 51))
        font2 = QFont()
        font2.setFamilies([u"Tw Cen MT Condensed Extra Bold"])
        font2.setPointSize(24)
        self.pushButton_2.setFont(font2)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
        self.label_2.setText(QCoreApplication.translate("Dialog", u"Quick Scan ", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", u"Quick Scan System", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", u"Custom Scan", None))
    # retranslateUi




import sys
from PySide6.QtWidgets import QApplication, QDialog, QFileDialog

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create an instance of QDialog
    dialog = QDialog()

    # Create an instance of Ui_Dialog
    ui = Ui_Dialog()

    # Set up the UI
    ui.setupUi(dialog)


    # Connect the custom scan button to a slot
    def custom_scan_slot():
        # Open a file dialog for the user to select a directory
        directory = QFileDialog.getExistingDirectory(dialog, "Select Directory")
        if directory:
            if not hasattr(ui, 'output_label'):
                # Create a QLabel dynamically if it doesn't exist
                ui.output_label = QLabel(dialog)
                ui.output_label.setGeometry(QRect(180, 460, 600, 30))  # Adjust position and size as needed
                ui.output_label.setStyleSheet("color: green; font-size: 14px; font-family: sans-serif; font-weight: bold; background-color: white; border: 1px solid black; border-radius: 5px; padding: 5px;")
                ui.output_label.setAlignment(Qt.AlignCenter)
            ui.output_label.setText(f"Selected directory: {directory}")
            ui.output_label.show()
    

    ui.pushButton_2.clicked.connect(custom_scan_slot)


    # Show the dialog
    dialog.show()

    # Execute the application
    sys.exit(app.exec())