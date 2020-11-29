from PyQt5.QtCore import Qt, QSize, QTimer
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import (QApplication,
    QWidget, QLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QComboBox)

from hand import Hand
from score import Score
from result import Result

class RockPaperScissorsGame(QWidget):

    def __init__(self):
        super().__init__()

        # Display Layout
        displayLayout = QGridLayout()

        self.pcName = QLabel('PC')
        self.fontSize(self.pcName, 7)
        self.pcName.setAlignment(Qt.AlignCenter)
        displayLayout.addWidget(self.pcName, 0, 0, 1, 2)

        self.userName = QLabel('YOU')
        self.fontSize(self.userName, 7)
        self.userName.setAlignment(Qt.AlignCenter)
        displayLayout.addWidget(self.userName, 0, 3, 1, 2)

        self.displayPc = QLabel()
        self.displayPc.setFixedSize(300, 300)
        self.displayPc.setAlignment(Qt.AlignCenter)
        displayLayout.addWidget(self.displayPc, 1, 0, 1, 2)

        self.vsIcon = QLabel('VS')
        self.fontSize(self.vsIcon, 6)
        displayLayout.addWidget(self.vsIcon, 1, 2)

        self.displayUser = QLabel()
        self.displayUser.setFixedSize(300, 300)
        self.displayUser.setAlignment(Qt.AlignCenter)
        displayLayout.addWidget(self.displayUser, 1, 3, 1, 2)

        # Button Layout
        buttonLayout = QGridLayout()

        self.rockButton = QPushButton()
        self.rockButton.setIconSize(QSize(100, 100))
        self.rockButton.setIcon(QIcon(QPixmap('image/rock.png')))
        self.rockButton.clicked.connect(lambda: self.buttonClicked('rock'))
        buttonLayout.addWidget(self.rockButton, 0, 0)

        self.paperButton = QPushButton()
        self.paperButton.setIconSize(QSize(100, 100))
        self.paperButton.setIcon(QIcon(QPixmap('image/paper.png')))
        self.paperButton.clicked.connect(lambda: self.buttonClicked('paper'))
        buttonLayout.addWidget(self.paperButton, 0, 1)

        self.scissorsButton = QPushButton()
        self.scissorsButton.setIconSize(QSize(100, 100))
        self.scissorsButton.setIcon(QIcon(QPixmap('image/scissors.png')))
        self.scissorsButton.clicked.connect(lambda: self.buttonClicked('scissors'))
        buttonLayout.addWidget(self.scissorsButton, 0, 2)

        # Status Layout
        statusLayout = QGridLayout()

        self.matchLine = QLineEdit()
        self.matchLine.setReadOnly(True)
        self.matchLine.setFixedHeight(30)
        statusLayout.addWidget(QLabel('Match: '), 0, 0)
        statusLayout.addWidget(self.matchLine, 0, 1)

        self.displayTimer = QLineEdit()
        self.displayTimer.setReadOnly(True)
        self.displayTimer.setFixedHeight(30)
        statusLayout.addWidget(QLabel('Time: '), 1, 0)
        statusLayout.addWidget(self.displayTimer, 1, 1)

        self.scoreLine = QLineEdit()
        self.scoreLine.setReadOnly(True)
        self.scoreLine.setFixedHeight(30)
        self.scoreLine.setAlignment(Qt.AlignCenter)
        statusLayout.addWidget(QLabel('Score: '), 2, 0)
        statusLayout.addWidget(self.scoreLine, 2, 1)

        self.messageLine = QLineEdit()
        self.messageLine.setReadOnly(True)
        self.messageLine.setFixedHeight(40)
        self.fontSize(self.messageLine, 8)
        self.messageLine.setAlignment(Qt.AlignCenter)
        statusLayout.addWidget(self.messageLine, 3, 0, 1, 2)

        self.bestOfMatchs = {'Best Of 3 Match' : 2, 'Best Of 5 Match' : 3, 'Best Of 7 Match' : 4}
        self.bestOfMatch = QComboBox()
        self.bestOfMatch.addItems(self.bestOfMatchs)
        statusLayout.addWidget(self.bestOfMatch, 5, 0, 1, 2)

        self.newGameButton = QPushButton()
        self.newGameButton.setText('New Game')
        self.newGameButton.clicked.connect(self.newGame)
        self.newGameButton.setFixedSize(220, 50)
        statusLayout.addWidget(self.newGameButton, 6, 0, 1, 2)

        # Main Layout
        mainLayout = QGridLayout()
        mainLayout.addLayout(displayLayout, 0, 0)
        mainLayout.addLayout(buttonLayout, 1, 0)
        mainLayout.addLayout(statusLayout, 0, 1, 2, 1)
        mainLayout.setSizeConstraint(QLayout.SetFixedSize)

        self.setLayout(mainLayout)

        self.setWindowTitle('Rock Paper Scissors!')

        self.startGame()


    def startGame(self):
        self.messageLine.setText('R.P.S!')
        self.rockButton.setDisabled(True)
        self.paperButton.setDisabled(True)
        self.scissorsButton.setDisabled(True)


    def newGame(self):
        self.hand = Hand()
        self.score = Score()
        self.result = Result()
        self.targetScore = self.bestOfMatchs[self.bestOfMatch.currentText()]
        self.currentUserHand = ''
        self.match = 1

        self.displayPc.clear()
        self.displayUser.clear()
        self.messageLine.clear()
        self.scoreLine.setText(str(self.score.pcScore) + ' : ' + str(self.score.userScore))
        self.rockButton.setDisabled(False)
        self.paperButton.setDisabled(False)
        self.scissorsButton.setDisabled(False)
        self.loop()


    def loop(self):
        self.matchLine.setText('No.' + str(self.match))
        self.timeRemaning = 5
        self.repeater = QTimer()
        self.repeater.setInterval(1000)
        self.repeater.timeout.connect(self.timer)
        self.repeater.start()


    def timer(self):
        if self.timeRemaning == 0:
            self.repeater.stop()
            return self.main()
        else:
            self.displayTimer.setText(str(self.timeRemaning))
            self.timeRemaning -= 1


    def main(self):
        self.displayTimer.clear()
        currentPcHand = self.hand.randomPcHand()

        if self.currentUserHand == '':
            self.message = 'Choose your hand!'
        else:
            self.message = self.result.result(currentPcHand, self.currentUserHand)
            if self.message == 'WIN':
                self.score.increaseUserScore()
            elif self.message == 'LOSE':
                self.score.increasePcScore()
            self.displayPc.setPixmap(self.hand.getPcHand(currentPcHand))
            self.match += 1

        self.scoreLine.setText(str(self.score.pcScore) + ' : ' + str(self.score.userScore))
        self.messageLine.setText(self.message)
        self.currentUserHand = ''

        return self.gameEnd() if self.score.pcScore == self.targetScore or self.score.userScore == self.targetScore else self.delay()


    def buttonClicked(self, hand):
        self.currentUserHand = hand
        self.displayUser.setPixmap(self.hand.getUserHand(hand))


    def delay(self):
        delayTime = QTimer()
        delayTime.singleShot(1500, self.nextMatch)


    def nextMatch(self):
        self.displayPc.clear()
        self.displayUser.clear()
        self.messageLine.clear()
        return self.loop()


    def gameEnd(self):
        self.rockButton.setDisabled(True)
        self.paperButton.setDisabled(True)
        self.scissorsButton.setDisabled(True)
        return self.messageLine.setText('YOU WIN!') if self.score.userScore > self.score.pcScore else self.messageLine.setText('YOU LOSE')


    def fontSize(self, text, size):
        font = text.font()
        font.setPointSize(font.pointSize() + size)
        text.setFont(font)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())