"""Module provide access to the keyboard listener"""
import sys
import threading
from types import NoneType
from pynput import keyboard
from infi.systray import SysTrayIcon

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
    hideWindow = pyqtSignal(bool)
    keys_buffer = []

    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        self.mywindow = MainWindow()
        self.mainWindow.connect(self.mywindow.add_label)
        self.hideWindow.connect(self.mywindow.hide_window)
        

        # listener
        self.listener = keyboard.Listener(on_press=self.on_press,on_release=self.on_release)
        self.listener.start()  # start to listen on a separate thread
        # self.listener.join()  # remove if main thread is polling self.keys

        self.create_systray_icon()

        self.app.exec_()

    def create_systray_icon(self):
        menu_options = (("Start Overlay", None, self.show_overlay), ("Hide Overlay", None, self.hide_overlay))
        self.systray = SysTrayIcon('small.ico',"Overlay Py", menu_options, on_quit=self.quit_systray_callback)
        systray_thread = threading.Thread(target=self.systray.start)
        systray_thread.start()

    def quit_systray_callback(self, systray):
        self.mywindow.quit()
        return False  # stop listener

    def show_overlay(self, systray):
        self.hideWindow.emit(False)

    def hide_overlay(self, systray):
        self.hideWindow.emit(True)

    def on_press(self, key):
        # get VK
        vk = getattr(key, 'vk', -1)

        if vk == 81:
            # show the mainwindow
            self.hideWindow.emit(False)
        if vk == 87:
            # show the mainwindow
            self.hideWindow.emit(True)

        if key == keyboard.Key.esc:
            self.mywindow.quit()
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys

        print(k)
        presentable_key = convert_ctrl(str(k))
        if presentable_key not in self.keys_buffer and presentable_key != 'None':
            self.keys_buffer.append(presentable_key)
            self.mainWindow.emit(presentable_key)


    def on_release(self, key):
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        presentable_ley = convert_ctrl(str(k))
        if presentable_ley in self.keys_buffer:
            self.keys_buffer.remove(presentable_ley)
        