# -*- coding: utf-8 -*-
#! /usr/bin/python3

from PyQt5.QtWidgets import QDialog, QSystemTrayIcon, QMenu, QAction
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt, QCoreApplication, QTimer
from PyQt5.QtGui import QIcon

iCountDown = 0
iTime = 0

class MainUI(QDialog):
    def __init__(self):
        super(MainUI, self).__init__()
        loadUi('resources/ui/maindialog.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bStarted = False
        self.timer = QTimer(self)
        self.cnter = QTimer(self)

        self.timer.timeout.connect(self.monitor)
        self.cnter.timeout.connect(self.update_countdown)

        self.pauseAction = QAction("Start", self)
        self.exitAction = QAction("Exit", self)

        self.trayIconMenu = QMenu(self)
        self.trayIconMenu.addAction(self.pauseAction)
        self.trayIconMenu.addAction(self.exitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(self.trayIconMenu)
        self.trayIcon.setIcon(QIcon('resources/icons/clock.png'))
        self.trayIcon.setToolTip('Smart Clock')
        self.trayIcon.show()
        self.exitAction.triggered.connect(self.exit_app)
        self.pauseAction.triggered.connect(self.pause_clock)
        self.trayIcon.activated.connect(self.icon_clicked)

        self.UiALert = AlertUI(self.timer)

    def exit_app(self):
        self.trayIcon.setVisible(False)
        QCoreApplication.instance().quit()

    def icon_clicked(self, status):
        if status in (2, 3):
            self.show()

    def run_stop(self):
        global iCountDown, iTime
        iTime = int(self.lineTimer.text()) * 1000 * 60
        if self.bStarted:
            self.bStarted = False
            self.btDo.setText('Start')
            self.timer.stop()
            self.cnter.stop()
            self.pauseAction.setText('Restart')
        else:
            self.bStarted = True
            self.btDo.setText('Stop')
            self.timer.start(iTime)
            iCountDown = iTime
            self.cnter.start(1000)
            self.lcdCountDown.display(iTime/1000)
            self.pauseAction.setText('Stop')

    def pause_clock(self):
        self.run_stop()

    def update_countdown(self):
        global iCountDown
        if iCountDown > 0:
            iCountDown -= 1000
            self.lcdCountDown.display(iCountDown//1000)
            tipStr = 'Time Left: ' + str(iCountDown//60000) + 'min'
            self.trayIcon.setToolTip(tipStr)
        self.UiALert.update_warn()
    
    def minimize(self):
        self.hide()

    def monitor(self):
        self.lcdCountDown.display(0)
        self.timer.stop()
        self.UiALert.reset_warn()
        self.UiALert.show()

    def keyPressEvent(self, event):
        if  Qt.Key_Escape == event.key():
             self.hide()


class AlertUI(QDialog):
    def __init__(self, timer=None):
        super(AlertUI, self).__init__()
        loadUi('resources/ui/alert.ui', self)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowOpacity(0.95)

        self.timer = timer
        self.iWarnTime = 0

        self.cbDelay.addItems(['1','2','3','4','5','10'])
        self.cbDelay.setCurrentIndex(4)

    def reset_warn(self):
        self.iWarnTime = 1
        self.lbTimer.setText('1')

    def update_warn(self):
        self.lbTimer.setText(str(self.iWarnTime) + ' Sec')
        self.iWarnTime += 1
    
    def restart(self):
        global iTime, iCountDown
        self.hide()
        self.timer.start(iTime)
        iCountDown = iTime + 1000

    def delay(self):
        global iCountDown
        iDelay = int(self.cbDelay.currentText()) * 1000 * 60
        self.hide()
        self.timer.start(iDelay)
        iCountDown = iDelay + 1000

    def keyPressEvent(self, event):
        if  Qt.Key_Escape == event.key():
            pass  # Disable 'Escape'
