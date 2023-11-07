import os.path

from gui.components import create_label_widget

from gui import BASE_DIR
from PyQt5.QtWidgets import QMessageBox, QMenu, QWidget, QMainWindow
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QActionEvent
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from tabs.live_video_render import LiveVideoRender


class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        screen_size = app.screens()[0].size()
        self.setMinimumWidth(int(screen_size.width() / 2.5))
        self.setMinimumHeight(int(screen_size.height() / 2))

        self.loaded = None
        self.config = None

        self._generate_welcome_page()
        self.window_set()

    def window_set(self):
        self.setWindowTitle("MQP")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ffffff'))
        self.setPalette(palette)

        icon = QtGui.QIcon()
        icon.addFile(os.path.join(BASE_DIR, 'assets', 'logo.svg'), QtCore.QSize(16, 16))
        icon.addFile(os.path.join(BASE_DIR, 'assets', 'logo.svg'), QtCore.QSize(24, 24))
        icon.addFile(os.path.join(BASE_DIR, 'assets', 'logo.svg'), QtCore.QSize(32, 32))
        icon.addFile(os.path.join(BASE_DIR, 'assets', 'logo.svg'), QtCore.QSize(48, 48))
        icon.addFile(os.path.join(BASE_DIR, 'assets', 'logo.svg'), QtCore.QSize(256, 256))
        self.setWindowIcon(icon)

    def _generate_welcome_page(self):
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.layout.setSpacing(30)

        title = create_label_widget(
            f"Welcome to the Major Qualifying Project\nof Apollinaris Rowe and Landen Kovens!",
            "font:bold; font-size:24px;",
            margins=(0, 30, 0, 0)
        )
        self.layout.addWidget(title, alignment=Qt.AlignCenter)

        description = create_label_widget(
            "This Project hopes to use machine learning and robotics to supplement spinal cord injury recovery in mice."
            "\nThe machine learning uses two classification neural networks to identify whether the rat has spinal coord injury."
            "\nThe data from the model is then processed and delivered to the robotics system to aid recovery.",
            "fot-size:12px; text-align: center;",
            margins=(0, 0, 0, 0)
        )
        self.layout.addWidget(description, alignment=Qt.AlignCenter)

        self.layout_buttons = QtWidgets.QHBoxLayout()
        self.layout_buttons.setAlignment(Qt.AlignCenter | Qt.AlignCenter)

        self.load_project_a_button = QtWidgets.QPushButton('Load Model A')
        self.load_project_a_button.setFixedWidth(200)
        # self.load_project_a_button.clicked.connect(self._load_project('A'))
        self.layout_buttons.addWidget(self.load_project_a_button)

        self.load_project_b_button = QtWidgets.QPushButton('Load Model B')
        self.load_project_b_button.setFixedWidth(200)
        # self.load_project_b_button.clicked.connect(self._load_project('B'))
        self.layout_buttons.addWidget(self.load_project_b_ button)

        self.layout.addLayout(self.layout_buttons)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def _load_project(self, button):
        cwd = os.getcwd()
        config = QtWidgets.QFileDialog.getOpenFileName(
            self, "Select a Configuration File", cwd, "Config files (*.yaml)"
        )
        if not config:
            return
        if button == 'A':
            self.config[0] = config[0]
            self.loaded[0] = False if not config else True
        elif button == 'B':
            self.config[1] = config[0]
            self.loaded[1] = False if not config else True

        if self.loaded[0] and self.loaded[1]:
            self._load_tabs()

    def _load_tabs(self):
        self.tab_widget = QtWidgets.QTabWidget()
        self.tab_widget.setContentsMargins(0, 20, 0, 0)

        self.live_video_render = LiveVideoRender(
            root=self, parent=None, description="MQP - Live Video Rendering"
        )

        self.tab_widget.addTab(self.live_video_render, "Live Video Rendering")

