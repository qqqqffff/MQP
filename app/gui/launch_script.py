import os.path
import sys
import ctypes
import platform

import PyQt5.QtWidgets as QtWidgets
import qdarkstyle
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap

from gui import BASE_DIR


def launch_mqp_app():
    app = QtWidgets.QApplication(sys.argv)

    style_file = os.path.join(BASE_DIR, "style.qss")
    app.setStyleSheet(style_file)

    dark_stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(dark_stylesheet)

    from gui.window import MainWindow

    window = MainWindow(app)
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    app_id = 'wpi.mqp.sci.0.0.1d'
    if platform.platform() == 'Windows':
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(app_id)
    launch_mqp_app()

