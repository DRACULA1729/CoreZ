# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerRxceXM.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtWidgets import (QApplication, QDialog, QSizePolicy, QWidget)
from PySide6.QtMultimedia import QMediaPlayer
from PySide6 import QtCore, QtWidgets, QtMultimediaWidgets
from PySide6.QtUiTools import QUiLoader


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(823, 480)
        self.label = QVideoWidget(Dialog)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 821, 481))

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)
    # setupUi

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Dialog", None))
        self.label.setText("")
    # retranslateUi



class VideoDialog(QtWidgets.QDialog):
    def __init__(self):
        super(VideoDialog, self).__init__()
        loader = QUiLoader()
        ui_file = QtCore.QFile('C:/Users/theth/Desktop/CoreZ Project (WORKING)/UI Designs/Testwin.ui')
        #ui_file.open(QtCore.QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()

        # Find the promoted QVideoWidget in the UI
        self.video_widget = self.ui.findChild(QVideoWidget, 'videoWidgetName')

        # Set up the media player
        self.media_player = QMediaPlayer()
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile("C:/Users/theth/Desktop/WhatsApp Video 2025-01-13 at 15.01.33_241f58d2.mp4"))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = VideoDialog()
    dialog.ui.show()
    app.exec()
