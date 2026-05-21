from PySide6 import QtWidgets, QtCore, QtMultimediaWidgets
from PySide6.QtMultimedia import QMediaPlayer
from PySide6.QtMultimediaWidgets import QVideoWidget
from PySide6.QtCore import QUrl

class VideoDialog(QtWidgets.QDialog):
    def __init__(self):
        super(VideoDialog, self).__init__()
        QtWidgets.QUiLoader().load('path/to/your/ui_file.ui', self)

        # Find the promoted QVideoWidget in the UI
        self.video_widget = self.findChild(QVideoWidget, 'videoWidgetName')

        # Set up the media player
        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_widget)
        self.media_player.setSource(QUrl.fromLocalFile("path/to/your/video.mp4"))

if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    dialog = VideoDialog()
    dialog.show()
    app.exec()
