import os.path

from gui.components import create_label_widget

from gui import BASE_DIR
from PyQt5.QtWidgets import QMessageBox, QMenu, QWidget, QMainWindow
from PyQt5 import QtCore
from PyQt5.QtGui import QIcon, QActionEvent
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, app):
        super(MainWindow, self).__init__()
        self.app = app
        screen_size = app.screens()[0].size()
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()

        self.project = None
        self.loaded = False

        self._generate_welcome_page()
        # self.window_set()

    def window_set(self):
        self.setWindowTitle("MQP")

        palette = QtGui.QPalette()
        palette.setColor(QtGui.QPalette.Window, QtGui.QColor('#ffffff'))
        self.setPalette(palette)

        # icon = os.path.join(BASE_DIR, 'assets', 'logo.png')
        # self.setWindowIcon(QIcon(icon))

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
        description.setMinimumWidth(400)
        description.setWordWrap(True)
        self.layout.addWidget(description, alignment=Qt.AlignCenter)

        self.load_project_button = QtWidgets.QPushButton('Load Model')

        widget = QWidget()
        widget.setLayout(self.layout)