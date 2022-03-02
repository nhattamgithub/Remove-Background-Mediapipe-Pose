import cv2
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QPushButton,QVBoxLayout, QFileDialog
from remove_bg_module import *
import os

class Capture():
    def __init__(self):
        self.capturing = False
        self.image_array = []
        self.c = None
        self.bg_height = 0
        self.size = ()

    def setVideoFile(self, path):
        if self.c is not None:
            self.c.release()
            cv2.destroyAllWindows()
        self.c = cv2.VideoCapture(path)
        self.startCapture()

    def open_background(self):
        path = QtWidgets.QFileDialog.getOpenFileName()[0]
        self.background = cv2.imread(path)
        self.bg_height = self.background.shape[0]

    def startCapture(self):
        self.capturing = True
        cap = self.c
        while(self.capturing):
            ret, frame = cap.read()
            if self.bg_height:
                frame = remove_bg(frame, self.background)
            cv2.imshow("Capture", frame)
            height, width, layers = frame.shape
            self.size = (width,height)
            self.image_array.append(frame)
            cv2.waitKey(5)
        
        cv2.destroyAllWindows()

    def saveCapture(self):
        current_directory = os.getcwd()
        out = cv2.VideoWriter(current_directory + '/result.mp4',cv2.VideoWriter_fourcc(*'DIVX'), 24, self.size)
        for i in range(len(self.image_array)):
            out.write(self.image_array[i])

    def endCapture(self):
        self.capturing = False

    def pauseCapture(self):
        if cv2.waitKey(0) & 0xFF == ord('p'):  # Pause
            self.capturing = False

    def quitCapture(self):
        cap = self.c
        cv2.destroyAllWindows()
        cap.release()
        QtCore.QCoreApplication.quit()


class Window(QtWidgets.QWidget):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Control Panel')

        self.capture = Capture()
        self.open_button = QPushButton('Open Video', self)
        self.open_button.clicked.connect(self.open)

        
        self.open_bg = QPushButton('Open Background Image', self)
        self.open_bg.clicked.connect(self.capture.open_background)

        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.capture.startCapture)

        self.end_button = QPushButton('End', self)
        self.end_button.clicked.connect(self.capture.endCapture)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.capture.pauseCapture)

        self.save_button = QPushButton('Save', self)
        self.save_button.clicked.connect(self.capture.saveCapture)

        self.quit_button = QPushButton('Quit', self)
        self.quit_button.clicked.connect(self.capture.quitCapture)

        
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.open_button)
        vbox.addWidget(self.open_bg)
        vbox.addWidget(self.start_button)
        vbox.addWidget(self.end_button)
        vbox.addWidget(self.pause_button)
        vbox.addWidget(self.save_button)
        vbox.addWidget(self.quit_button)

        self.setLayout(vbox)
        self.setGeometry(100, 100, 200, 200)
        self.show()

    def open(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self)[0]
        if path:
            self.capture.setVideoFile(path)

    

if __name__== '__main__':
    import sys
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())