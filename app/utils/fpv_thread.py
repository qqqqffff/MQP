import cv2
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage


class WorkerThread(QThread):
    def __init__(self):
        super().__init__()
        self.image_update = pyqtSignal(QImage)
        self.thread_active = False

    def run(self):
        self.thread_active = True
        capture = cv2.VideoCapture(0)

        while self.thread_active:
            ret, frame = capture.read()
            if ret:
                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                convert = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
                pic = convert.scaled(640, 480, Qt.KeepAspectRatio)
                self.image_update.emit(pic)

    def stop(self):
        self.thread_active = False
        self.quit()

