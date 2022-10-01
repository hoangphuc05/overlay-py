import sys
from types import NoneType

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QSpacerItem
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QEasingCurve, QEventLoop, QVariantAnimation, QVariant, QTimer, pyqtSignal, pyqtSlot, Qt, QObject
from pynput import keyboard

COLUMN_COUNT = 5

# https://stackoverflow.com/questions/56483841/error-while-changing-qobject-stylesheet-in-a-thread
class AnimationLabel(QLabel):
    redrawEvent = pyqtSignal()
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.animation = QVariantAnimation()
        self.animation.valueChanged.connect(self.changeColor)
        self.parentList = args[0].char_widget
        self.redrawEvent.connect(args[0].redrawMain)
        QTimer.singleShot(3000, self.startFadeOut)
        self.mAnimation = QVariantAnimation(
            self,
            startValue=QColor(0,0,0, 175),
            endValue=QColor(0,0,0,0),
            duration=1000,
            valueChanged=self.on_color_change,
        )
        self.mAnimation.setEasingCurve(QEasingCurve.InOutQuad)

    def suicide(self):
        self.setParent(None)
        self.parentList.remove(self)
        self.redrawEvent.emit()
        del self

    def startFadeOut(self):
        self.mAnimation.start()
        QTimer.singleShot(900, self.suicide)

    @pyqtSlot(QtCore.QVariant)
    @pyqtSlot(QtGui.QColor)
    def on_color_change(self, color: QtGui.QColor):
        self.setStyleSheet(styleBase.format(color.getRgb(), QColor(255,255,255,color.alpha()).getRgb()))

    @pyqtSlot(QVariant)
    def changeColor(self, color):
        palette = self.palette()
        palette.setColor(QPalette.ColorRole.Window, color)
        self.setPalette(palette)

    def startFadeIn(self):
        self.animation.stop()
        self.animation.setStartValue(QColor(0, 0, 0, 0))
        self.animation.setEndValue(QColor(0, 0, 0, 255))
        self.animation.setDuration(2000)
        self.animation.setEasingCurve(QEasingCurve.InBack)
        self.animation.start()

    # def startFadeOut(self):
    #     self.animation.stop()
    #     self.animation.setStartValue(QColor(0, 0, 0, 255))
    #     self.animation.setEndValue(QColor(0, 0, 0, 0))
    #     self.animation.setDuration(2000)
    #     self.animation.setEasingCurve(QEasingCurve.OutBack)
    #     self.animation.start()

    def startAnimation(self):
        self.startFadeIn()
        loop = QEventLoop()
        self.animation.finished.connect(loop.quit)
        loop.exec_()
        QTimer.singleShot(2000, self.startFadeOut)

styleBase = '''background-color:  rgba{0};
                width: 50px; height: 50px;
                font: 25px;
                border-radius: 15px;
                margin: 15px;
                padding: 15px;
                color: rgba{1};'''

class MainWindow(QMainWindow):
    diffX = 0
    diffY = 0
    def __init__(self):
        QMainWindow.__init__(self)
        self.char_history = []
        self.char_widget = []
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
        self.widget = QWidget()
        self.mLayout = QGridLayout()
        
        # for i in range(len(self.char_history)):
        #     localWidget = AnimationLabel(self)
        #     # localWidget.setWindowOpacity(0.1)
        #     localWidget.setFixedSize(150, 150)
        #     localWidget.setAlignment(Qt.AlignCenter)
        #     localWidget.setFont(QtGui.QFont(".", 25))
        #     localWidget.setAutoFillBackground(True)
        #     localWidget.setStyleSheet(styleBase.format(QColor(0,0,0, 175).getRgb(), QColor(255, 255, 255, 175).getRgb() ))
        #     # palette = localWidget.palette()
        #     # palette.setColor(QPalette.ColorRole.Foreground ,QColor(255,255,255, 123))
        #     # palette.setColor(QPalette.ColorRole.Base ,QColor(0, 0, 0, 100))
        #     # localWidget.setOpa(0.9)
        #     # localWidget.setPalette(palette)

        #     self.mLayout.addWidget(localWidget,1, i+1)
        #     self.char_widget.append(localWidget)



        # self.mLayout.addWidget(self.keyWidget)
        self.widget.setLayout(self.mLayout)
        self.setCentralWidget(self.widget)
        self.show()

    def mousePressEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            self.diffX = self.pos().x() - event.globalPos().x()
            self.diffY = self.pos().y() - event.globalPos().y()

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.LeftButton:
            # print(event.globalPos().x(), event.globalPos().y())
            self.move(event.globalPos().x() + self.diffX, event.globalPos().y() + self.diffY)

    def addLabel(self, key):
        print(key)
        localWidget = AnimationLabel(self)
        localWidget.setFixedSize(150, 150)
        localWidget.setAlignment(Qt.AlignCenter)
        localWidget.setStyleSheet(styleBase.format(QColor(0,0,0, 200).getRgb(), QColor(255, 255, 255, 255).getRgb() ))
        localWidget.setText(key)
        self.char_widget.append(localWidget)
        self.redrawMain()
    
    def redrawMain(self):
        for i in reversed(range(self.mLayout.count())): 
            if (self.mLayout.itemAt(i).widget() != None):
                self.mLayout.itemAt(i).widget().setParent(None) 
            else:
                self.mLayout.removeItem(self.mLayout.itemAt(i))

        del self.char_widget[:-5]
        for i in range(len(self.char_widget)):
            self.mLayout.addWidget(self.char_widget[i], 1, i+1)
        # fill up the rest of column with empty space
        for i in range(COLUMN_COUNT, len(self.char_widget), -1):
            self.mLayout.addItem(QSpacerItem(110, 110, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding), 1, i)


    # def addKey(self, key, sut):
    #     self.char_history.insert(0,key)
    #     del self.char_history[4:]
    #     for i in range(len(self.char_history)):
    #         self.char_widget[i].setText(self.char_history[i])
        # sut.makeConnect(self.char_widget[0].startAnimation)
        

        # self.char_widget[0].startAnimation()

    def quit(sef):
        QtWidgets.qApp.quit()

class KeyboardListener(QObject):
    keypress = pyqtSignal()
    mainWindow = pyqtSignal(str)

    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.mywindow = MainWindow()
        self.mainWindow.connect(self.mywindow.addLabel)
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
        # print("a")
        if key == keyboard.Key.esc:
            self.mywindow.quit()
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        # self.mywindow.addKey(k, self)
        # print('Key pressed: ' + str(key))
        self.mainWindow.emit(k.capitalize())
    
    def makeConnect(self, connection):
        self.keypress.connect(connection)

    def registerMainWindow(self, window):
        self.mainWindow.connect(window)
        

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
    