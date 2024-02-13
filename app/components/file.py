from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QCheckBox,
                             QSlider, QStyle, QStatusBar)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget

class FileMode(QWidget):
    def __init__(self, parent=None):
        super(FileMode, self).__init__(parent)

        self.media_player = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        video_widget = QVideoWidget()
        video_widget.setFixedSize(800, 450)

        open_button = QPushButton("Open Video")
        open_button.setStyleSheet("width: 100; height: 25;")
        open_button.clicked.connect(self.open_video)

        self.play_button = QPushButton()
        self.play_button.setEnabled(False)
        self.play_button.setStyleSheet("width: 25; height: 25;")
        self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.play_button.clicked.connect(self.play)

        self.position_slider = QSlider(Qt.Horizontal)
        self.position_slider.setRange(0, 0)
        self.position_slider.sliderMoved.connect(self.set_position)

        self.open_model_button = QPushButton("Open Model")
        self.open_model_button.setStyleSheet("width: 100; height: 25;")
        self.open_model_button.clicked.connect(self.open_model)

        self.status_bar = QStatusBar()
        self.status_bar.setStyleSheet("height: 25;")

        self.model_runner_cb = QCheckBox("Apply Model")
        self.model_runner_cb.setEnabled(False)
        self.model_runner_cb.setChecked(False)
        self.model_runner_cb.stateChanged.connect(self.apply_model)

        controls_layout = QHBoxLayout()
        controls_layout.setContentsMargins(25, 0, 400, 0)
        controls_layout.setSpacing(10)
        controls_layout.addWidget(open_button)
        controls_layout.addWidget(self.play_button)
        controls_layout.addWidget(self.position_slider)

        params_layout = QHBoxLayout()
        params_layout.setContentsMargins(25, 0, 25, 0)
        params_layout.setSpacing(10)
        params_layout.addWidget(self.open_model_button)
        params_layout.addWidget(self.model_runner_cb)
        params_layout.addWidget(self.status_bar)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(video_widget)
        layout.addLayout(controls_layout)
        layout.setAlignment(controls_layout, Qt.AlignBottom)
        layout.addLayout(params_layout)
        layout.setAlignment(params_layout, Qt.AlignBottom)

    def open_video(self):
        file, _ = QFileDialog.getOpenFileName(self, "Select Video", ".", "Video Files (*.mp4 *.flv *.ts *.mts *.avi)")
        if file:
            self.media_player.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.play_button.setEnabled(True)
            self.status_bar.showMessage("Read: " + file)

    def play(self):
        if self.media_player.state() == QMediaPlayer.PlayingState:
            self.media_player.pause()
        else:
            self.media_player.play()

    def media_state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.play_button.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.position_slider.setValue(position)

    def duration_changed(self, duration):
        self.position_slider.setRange(0, duration)

    def set_position(self, position):
        self.media_player.setPosition(position)

    def handle_error(self):
        self.play_button.setEnabled(False)

    def apply_model(self, state):
        if state == 2:
            self.status_bar.showMessage("Model Activated")
        else:
            self.status_bar.showMessage("Model Deactivated")
