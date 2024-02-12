from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QFileDialog, QSlider, QHBoxLayout
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget


class Application(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("MQP")
        self.setGeometry(100, 100, 1280, 800)

        self.open_video_button = QPushButton("Select Video", self)
        self.open_video_button.setStyleSheet("width: 200; height: 40;")

        self.open_video_button.clicked.connect(self.open_video)

        self.video_player = QVideoWidget(self)
        # self.video_player.setStyleSheet("width: 600; height: 600;")

        self.play_button = QPushButton("Play")
        self.play_button.setEnabled(False)
        self.play_button.setStyleSheet("width: 25; height: 25;")
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.setPosition)

        controlLayout = QHBoxLayout()
        controlLayout.addWidget(self.play_button)
        controlLayout.addWidget(self.position_slider)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.media_player.setVideoOutput(self.video_player)

        layout = QVBoxLayout()
        layout.addWidget(self.video_player)
        layout.addLayout(controlLayout)
        layout.addWidget(self.open_video_button)
        layout.setAlignment(self.media_player, Qt.AlignCenter)
        layout.setAlignment(self.open_video_button, Qt.AlignCenter)
        self.setLayout(layout)
        self.show()

    def open_video(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        filename, _ = QFileDialog.getOpenFileName(self, "Choose Video File", "", "MP4 Files (*.mp4)", options=options)
        if filename:
            print("Selected File: ", filename)
            media_content = QMediaContent(QUrl.fromLocalFile(filename))
            self.media_player.setMedia(media_content)
            self.media_player.play()

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def setPosition(self):
        print("test")

    def duration_change(self):
        print("test")