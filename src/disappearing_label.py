"""Module provide A QTLabel that disappear after a while"""

from PyQt5 import QtGui, QtCore
from PyQt5.QtWidgets import  QLabel, QSizePolicy
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtCore import QEasingCurve, QVariantAnimation, QVariant, QTimer, pyqtSignal, pyqtSlot
# from pynput import keyboard
from const import STYLEBASE


class DisappearingLabel(QLabel):
    """QLabel that disappear after a while"""
    fading = False
    redrawEvent = pyqtSignal()
    def __init__(self, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        self.parent_list = args[0].char_widget
        self.redrawEvent.connect(args[0].redraw_main)
        QTimer.singleShot(1500, self.start_fade_out)
        self.m_animation = QVariantAnimation(
            self,
            startValue=QColor(0,0,0, 175),
            endValue=QColor(0,0,0,0),
            duration=1000,
            valueChanged=self.on_color_change,
        )
        self.m_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def self_destruct(self):
        """Remove itself from parent list then attempt to kill itself"""
        self.setParent(None)
        self.parent_list.remove(self)
        self.redrawEvent.emit()
        del self

    # def graduate(self):
    #     """remove early"""
    #     self.m_animation = QVariantAnimation(
    #         self,
    #         startValue=QColor(0,0,0, 175),
    #         endValue=QColor(0,0,0,0),
    #         duration=100,
    #         valueChanged=self.on_color_change,
    #     )
    #     self.m_animation.setEasingCurve(QEasingCurve.InOutQuad)
    #     self.start_fade_out()

    def start_fade_out(self):
        """Start the fadeout process, then call suicide after a while"""
        if self.fading is True:
            return
        self.m_animation.start()
        QTimer.singleShot(900, self.self_destruct)

    @pyqtSlot(QtCore.QVariant)
    @pyqtSlot(QtGui.QColor)
    def on_color_change(self, color: QtGui.QColor):
        """Handle color changes"""
        self.setStyleSheet(STYLEBASE.format(color.getRgb(), QColor(255,255,255,color.alpha()).getRgb()))
