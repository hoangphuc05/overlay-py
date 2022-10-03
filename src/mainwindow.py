"""Module allow access to MainWindow class"""


from os import path

from xmlrpc.client import Boolean
from PyQt5 import QtCore
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMainWindow, QWidget, QGridLayout, QSpacerItem, QBoxLayout, QHBoxLayout
from PyQt5.QtGui import QColor, QIcon
from PyQt5.QtCore import Qt

from disappearing_label import DisappearingLabel
from const import COLUMN_COUNT, STYLEBASE

class MainWindow(QMainWindow):
    """The main window that act as the overlay."""
    diff_x = 0
    diff_y = 0
    def __init__(self):
        QMainWindow.__init__(self)
        bundle_dir = path.abspath(path.dirname(__file__))
        self.setWindowIcon(QIcon(path.join(bundle_dir, 'small.ico')))
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
                QtCore.QSize(1920, 200),
                QtWidgets.qApp.desktop().availableGeometry()
        ))
        self.widget = QWidget()
        # self.m_layout = QGridLayout()
        self.m_layout = QHBoxLayout()


        self.widget.setLayout(self.m_layout)
        self.setCentralWidget(self.widget)
        self.show()

    def mousePressEvent(self, event):
        """React to mouse press event,
           used to calculate position of the mouse before moving the window."""
        if event.buttons() & Qt.LeftButton:
            self.diff_x = self.pos().x() - event.globalPos().x()
            self.diff_y = self.pos().y() - event.globalPos().y()

    def mouseMoveEvent(self, event):
        """Handle mouse drag event, used to move the window."""
        if event.buttons() & Qt.LeftButton:
            # print(event.globalPos().x(), event.globalPos().y())
            self.move(event.globalPos().x() + self.diff_x, event.globalPos().y() + self.diff_y)

    def add_label(self, key):
        """Add a label to the window."""
        local_widget = DisappearingLabel(self)
        # local_widget.setFixedSize(150, 150)
        local_widget.setAlignment(Qt.AlignCenter)
        local_widget.setStyleSheet(STYLEBASE.format(QColor(0,0,0, 200).getRgb(), QColor(255, 255, 255, 255).getRgb() ))
        local_widget.setText(key)
        self.char_widget.append(local_widget)
        self.redraw_main()

    def redraw_main(self):
        """Redraw the main window."""
        for i in reversed(range(self.m_layout.count())): 
            if self.m_layout.itemAt(i).widget() is not None:
                self.m_layout.itemAt(i).widget().setParent(None)
            else:
                self.m_layout.removeItem(self.m_layout.itemAt(i))

        del self.char_widget[:-5]

        for i in range(len(self.char_widget)):
            self.m_layout.addWidget(self.char_widget[i],Qt.AlignLeft )
        self.m_layout.addStretch()
        # fill up the rest of column with empty space
        # for i in range(COLUMN_COUNT, len(self.char_widget), -1):
        #     self.m_layout.addItem(QSpacerItem(177, 100, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

    def hide_window(self, flag: bool):
        """Hide or show the main window"""
        if flag:
            self.hide()
        else:
            self.show()

    def quit(self):
        """Exit the window."""
        QtWidgets.qApp.quit()
