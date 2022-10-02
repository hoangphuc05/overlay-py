"""Module provide access to the keyboard listener"""
import sys
from types import NoneType
from pynput import keyboard

from PyQt5 import QtGui, QtCore, uic
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QGridLayout, QLabel, QSpacerItem
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QEasingCurve, QEventLoop, QVariantAnimation, QVariant, QTimer, pyqtSignal, pyqtSlot, Qt, QObject

from mainwindow import MainWindow
from ctrl_convert import convert_ctrl
class KeyboardListener(QObject):
    keypress = pyqtSignal()
    mainWindow = pyqtSignal(str)
    keys_buffer = []

    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.mywindow = MainWindow()
        self.mainWindow.connect(self.mywindow.add_label)
        # layout = QVBoxLayout()
        # layout.addWidget(QPushButton('uwu'))
        # widget = QWidget()
        # widget.setLayout(layout)
        # self.mywindow.setCentralWidget(widget)
        # self.mywindow.show()

        # listener
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
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
        # print('Key pressed: ' + convert_ctrl(str(key)))
        presentable_ley = convert_ctrl(str(k))
        if presentable_ley not in self.keys_buffer:
            self.keys_buffer.append(presentable_ley)
            self.mainWindow.emit(presentable_ley)


    def on_release(self, key):
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        presentable_ley = convert_ctrl(str(k))
        if presentable_ley in self.keys_buffer:
            self.keys_buffer.remove(presentable_ley)
        