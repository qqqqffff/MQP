import os.path

import cv2
from matplotlib import pyplot as plt
from gui.components import DefaultTab
from utils.fpv_thread import WorkerThread
from PyQt5.QtWidgets import QPushButton, QHBoxLayout
from PyQt5.QtGui import QImage
from PyQt5.QtCore import Qt
from gui import BASE_DIR


class LiveVideoRender(DefaultTab):
    def __init__(self, root, parent, description):
        super().__init__(root, parent, description)
        self.video_feed = None
        self._set_page()
        self.video_thread = WorkerThread()
        self.video_thread.image_update.connect(self.image_update_slot)

    def _set_page(self):
        self.video_controls = QHBoxLayout()
        self.video_controls.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.video_controls.setSpacing(20)
        self.video_controls.setContentsMargins(20, 0, 0, 0)

        self.stop_feed_button = QPushButton()
        self.stop_feed_button.clicked.connect(self.stop_feed)
        self.video_controls.addWidget(self.stop_feed_button)

        self.start_feed_button = QPushButton()
        self.start_feed_button.clicked.connect(self.start_feed)
        self.video_controls.addWidget(self.start_feed_button)
        self.main_layout.addWidget(self.video_controls)

        self.video_feed = QImage(os.path.join(BASE_DIR, "assets", "camera-error-placeholder.png"))
        self.video_feed.scaled(640, 480, Qt.KeepAspectRatio)
        self.main_layout.addWidget(self.video_feed)

    def stop_feed(self):
        self.video_thread.stop()

    def start_feed(self):
        self.video_thread.start()

    def image_update_slot(self, image):
        self.video_feed = QImage(image)

