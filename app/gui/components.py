from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt


def create_label_widget(
        text: str,
        style: str = "",
        margins: tuple = (20, 10, 0, 10),
) -> QtWidgets.QLabel:

    label = QtWidgets.QLabel(text)
    label.setContentsMargins(*margins)
    label.setStyleSheet(style)

    return label


def create_horizontal_layout(
    alignment=None, spacing: int = 20, margins: tuple = (20, 0, 0, 0)
) -> QtWidgets.QHBoxLayout():

    layout = QtWidgets.QHBoxLayout()
    layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    layout.setSpacing(spacing)
    layout.setContentsMargins(*margins)

    return layout


class DefaultTab(QtWidgets.QWidget):
    def __init__(
        self,
        root: QtWidgets.QMainWindow,
        parent: QtWidgets.QWidget = None,
        description: str = ''
    ):
        super(DefaultTab, self).__init__(parent)

        self.parent = parent
        self.root = root

        self.description = description
        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setLayout(self.main_layout)

        self._init_default_layout()

    def _init_default_layout(self):
        self.main_layout.addWidget(
            create_label_widget(self.description, "font:bold;", (10, 10, 0, 0))
        )

        self.seperator = QtWidgets.QFrame()
        self.seperator.setFrameShape(QtWidgets.QFrame.HLine)
        self.seperator.setFrameShadow(QtWidgets.QFrame.Raised)
        self.seperator.setLineWidth(0)
        self.seperator.setMidLineWidth(1)
        policy = QtWidgets.QSizePolicy()
        policy.setVerticalPolicy(QtWidgets.QSizePolicy.Policy.Fixed)
        policy.setHorizontalPolicy(QtWidgets.QSizePolicy.Policy.MinimumExpanding)
        self.seperator.setSizePolicy(policy)
        self.main_layout.addWidget(self.seperator)

