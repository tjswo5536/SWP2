from PyQt5.QtGui import QPixmap
import random

class Hand:

    def __init__(self):
        self.userHands = {'rock': 'image/rock.png', 'paper': 'image/paper.png', 'scissors': 'image/scissors.png'}
        self.pcHands = {'rock': 'image/reversedRock.png', 'paper': 'image/reversedPaper.png', 'scissors': 'image/reversedScissors.png'}
        self.userHand = QPixmap()
        self.pcHand = QPixmap()


    def randomPcHand(self):
        return random.choice(list(self.pcHands.keys()))


    def getPcHand(self, currentPcHand):
        self.pcHand.load(self.pcHands[currentPcHand])
        self.pcHand = self.pcHand.scaled(250, 250)
        return self.pcHand


    def getUserHand(self, hand):
        self.userHand.load(self.userHands[hand])
        self.userHand = self.userHand.scaled(250, 250)
        return self.userHand