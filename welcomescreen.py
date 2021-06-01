import sys
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
from PyQt5.QtGui import QPixmap
import gr_aut_task
import aut_gr_task
import morsiphier


def execute_message_box(text,windowTitle):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Warning)
    msgBox.setText(text)
    msgBox.setWindowTitle(windowTitle)
    msgBox.setStandardButtons(QMessageBox.Ok)
    msgBox.exec()


class WelcomeScreen(QDialog):
    def __init__(self,widget):
        super(WelcomeScreen, self).__init__()
        loadUi('gui/welcomeScreen.ui', self)
        self.widget=widget
        self.gr_to_aut.clicked.connect(self.goto_gr_aut_task)
        self.aut_to_gr.clicked.connect(self.goto_aut_gr_task)
        self.morsiphier_btn.clicked.connect(self.morsiphier)

    def morsiphier(self):
        morsiphier_screen = morsiphier.Morsiphier(self.widget)
        self.widget.addWidget(morsiphier_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def goto_aut_gr_task(self):
        aut_gr_screen = aut_gr_task.AutomataGrammarTask(self.widget)
        self.widget.addWidget(aut_gr_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)

    def goto_gr_aut_task(self):
        gr_aut_screen = gr_aut_task.GrammarAutomataTask(self.widget)
        self.widget.addWidget(gr_aut_screen)
        self.widget.setCurrentIndex(self.widget.currentIndex()+1)