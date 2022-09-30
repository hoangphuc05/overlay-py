import sys

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QEasingCurve, QEventLoop, QVariantAnimation, QVariant, QTimer
from pynput import keyboard

class AnimationLabel(QLabel):
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.changeColor)

    @pyqtSlot(QVariant)
    def changeColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.WindowText, color)
        self.setPalette(palette)

    def startFadeIn(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 0))
        self.animation.setEndValue(QColor(0, 0, 0, 255))
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.start()

    def startFadeOut(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 255))
        self.animation.setEndValue(QColor(0, 0, 0, 0))
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.OutBack)
        self.animation.start()

    def startAnimation(self):
        self.startFadeIn()
        loop = QEventLoop()
        self.animation.finished.connect(loop.quit)
        loop.exec_()
        QTimer.singleShot(2000, self.startFadeOut)


class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint |
            QtCore.Qt.FramelessWindowHint |
            QtCore.Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setGeometry(
            QtWidgets.QStyle.alignedRect(
                QtCore.Qt.LeftToRight, QtCore.Qt.AlignCenter,
                QtCore.QSize(400, 200),
                QtWidgets.qApp.desktop().availableGeometry()
        ))
        widget = QWidget()
        self.mLayout = QGridLayout()
        
        self.keyWidget = QLabel(self)
        self.keyWidget.setWindowOpacity(0.2)
        self.keyWidget.setStyleSheet("background-color:  rgba(0, 0, 0, 60);"
                                     "font: bold 35px;"
                                     "margin: 15px;"
                                     "color: white;"
        )


        self.mLayout.addWidget(self.keyWidget)
        widget.setLayout(self.mLayout)
        self.setCentralWidget(widget)
        self.show()

    def mousePressEvent(self, event):
        QtWidgets.qApp.quit()
    def addKey(self, key):
        self.keyWidget.setText(key)
        # self.mLayout.addWidget(keyWidget)
    def quit(sef):
        QtWidgets.qApp.quit()

class KeyboardListener():
    def __init__(self) -> None:
        self.app = QApplication(sys.argv)
        self.mywindow = MainWindow()
        # layout = QVBoxLayout()
        # layout.addWidget(QPushButton('uwu'))
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.mywindow.setCentralWidget(widget)
        # self.mywindow.show()

        # listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()  # start to listen on a separate thread
        # self.listener.join()  # remove if main thread is polling self.keys

        self.app.exec_()

    def on_press(self, key):
        print("a")
        if key == keyboard.Key.esc:
            self.mywindow.quit()
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        self.mywindow.addKey(k)
        print('Key pressed: ' + str(key))
        

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # mywindow = MainWindow()
    # layout = QVBoxLayout()
    # layout.addWidget(QPushButton('uwu'))
    # widget = QWidget()
    # widget.setLayout(layout)
    # mywindow.setCentralWidget(widget)
    # mywindow.show()
    # app.exec_()
    KeyboardListener()
    