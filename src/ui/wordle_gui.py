import sys
import os

sys.path.append(os.getcwd()[0:len(os.getcwd()) - 7])

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QApplication, QStyleFactory
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt
from src import Wordle as Wordle
from src.Wordle import Match
from src.Wordle import Status

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.widgets = [([0]*Wordle.WORD_SIZE) for j in range(Wordle.MAX_TRIES)]

        MainWindow.setObjectName("MainWindow")

        sizeObject = QtWidgets.QDesktopWidget().screenGeometry(-1)
        self.length = int(str(sizeObject.width()))
        self.width = int(sizeObject.height())


        MainWindow.resize(self.length, self.width)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.label = QtWidgets.QLabel(self)
        self.label.setText("WORDLE")
        self.label.move(int(0.424*self.length), int(0.067*self.width))
        labelFont = self.label.font()
        labelFont.setPointSize(40)
        self.label.setFont(labelFont)
        self.label.setStyleSheet("color: white")
        self.label.adjustSize()

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(int(0.35417*self.length), int(0.212*self.width),
                                                       int(0.251*self.length), int(0.4345*self.width)))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")

        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")

        for i in range(len(self.widgets)):
            for j in range(len(self.widgets[0])):
                self.widgets[i][j] = QtWidgets.QTextBrowser(self.gridLayoutWidget)
                self.gridLayout.addWidget(self.widgets[i][j], i, j, 1, 1)
                self.widgets[i][j].setFont(QFont("helvetica", 50))
                self.widgets[i][j].setAlignment(Qt.AlignCenter)
                self.widgets[i][j].setTextColor(QColor(255,255,255))
                self.widgets[i][j].setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.widgets[i][j].setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
                self.widgets[i][j].setStyleSheet("background-color: #000000;"
                                                 "border: 2px solid #3c393b;"
                                                 "margin-top:0px; "
                                                 "margin-bottom:0px; "
                                                 "margin-left:0px; margin-right:0px; "
                                                 "-qt-block-indent:0; "
                                                 "text-indent:0px;")


        self.guessButton = QtWidgets.QPushButton(self.centralwidget)
        self.guessButton.setGeometry(QtCore.QRect(int(0.40764*self.length), int(0.667*self.width),
                                                  int(0.14653*self.length), int(0.1012*self.width)))
        self.guessButton.setObjectName("guessButton")
        font = self.guessButton.font()
        font.setPointSize(30)
        self.guessButton.setFont(font)
        self.guessButton.setStyleSheet("background-color: grey");
        self.guessButton.setEnabled(False)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, self.length, int(0.0245*self.width)))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Wordle Game"))
        self.guessButton.setText(_translate("MainWindow", "GUESS"))

class wordleGUI(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent=parent)
        self.setupUi(self)
        self.setStyleSheet("background-color: #121214;")
        self.guessButton.clicked.connect(self.guessButtonClicked)
        self.currentRow = 0
        self.currentCol = 0
        self.target = Wordle.TARGET_WORD
        self.status = Status.IN_PROGRESS

    def enableGuessButton(self):
        self.guessButton.setEnabled(True)
        self.guessButton.setStyleSheet("background-color: #527d9c; color: white;");

    def disableGuessButton(self):
        self.guessButton.setEnabled(False)
        self.guessButton.setStyleSheet("background-color: grey");

    def addText(self, event):
        self.widgets[self.currentRow][self.currentCol].setText(event.text().upper())
        self.widgets[self.currentRow][self.currentCol].setAlignment(Qt.AlignCenter)
        self.currentCol += 1

    def isKeyLetter(self, event):
        return event.key() in range(65, 91) or event.key() in range(97, 123)

    def pressLetter(self, event):
        if self.currentCol in range(0, Wordle.WORD_SIZE):
            self.addText(event)
            if self.currentCol >= Wordle.WORD_SIZE:
                self.enableGuessButton()

    def pressBackspace(self):
        if self.currentCol in range(1, Wordle.WORD_SIZE + 1):
            self.currentCol -= 1
            self.widgets[self.currentRow][self.currentCol].setText("")
            self.disableGuessButton()

    #def pressEnter(self):
    #    if self.currentCol >= Wordle.WORD_SIZE:
    #        self.guessButtonClicked()

    def keyPressEvent(self, event):
        if self.status == Status.IN_PROGRESS:
            if self.isKeyLetter(event):
                self.pressLetter(event)
            elif event.key() == QtCore.Qt.Key_Backspace:
                self.pressBackspace()
            #elif event.key() == QtCore.Qt.Key_Return:
            #    self.pressEnter()

    def createGuess(self):
        guess = ""
        for widget in self.widgets[self.currentRow]:
            guess += widget.toPlainText()
        return guess

    def guessButtonClicked(self):
        guess = self.createGuess()
        tally_output = Wordle.tally(self.target, guess)
        self.colorCode(tally_output)
        self.currentRow += 1
        self.currentCol = 0
        self.disableGuessButton()
        self.status = Wordle.determine_status(tally_output, self.currentRow)
        if self.status == Status.WON or self.status == Status.LOST:
            self.disableGuessButton()
            self.showPopup(Wordle.create_message(self.currentRow, self.status, self.target))

    def colorCode(self, tally_output):
        for i in range(len(tally_output)):
            self.widgets[self.currentRow][i].setStyleSheet("background-color: #3a3a3c;")
            if tally_output[i] == Match.EXACT:
                self.widgets[self.currentRow][i].setStyleSheet("background-color: #528d4d;")
            elif tally_output[i] == Match.MATCH:
                self.widgets[self.currentRow][i].setStyleSheet("background-color: #b59f3a;")


    def showPopup(self, message):
        popup = QMessageBox()
        popup.setWindowTitle("Game Over")
        popup.setText(message)

        x = popup.exec_()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle(QStyleFactory.create("fusion"))
    ui = wordleGUI()
    ui.show()
    sys.exit(app.exec_())
