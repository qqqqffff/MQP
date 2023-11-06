import os.path
import sys

import PyQt5.QtWidgets as QtWidgets
import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from gui import BASE_DIR


def launch_mqp_app():
    app = QtWidgets.QApplication(sys.argv)
    # app.setWindowIcon(QIcon(os.path.join(BASE_DIR, "assets", "logo.png")))
    screen_size = app.screens()[0].size()

    stylefile = os.path.join(BASE_DIR, "style.qss")
    with open(stylefile, "r") as f:
        app.setStyleSheet(stylefile)

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)

    from gui.window import MainWindow

    window = MainWindow(app)
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    launch_mqp_app()