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

