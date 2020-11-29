class Result:

    def result(self, currentPcHand, currentUserHand):
        if currentPcHand == 'rock':
            if currentUserHand == 'paper':
                return 'WIN'
            elif currentUserHand == 'scissors':
                return 'LOSE'
            else:
                return 'DRAW'

        elif currentPcHand == 'paper':
            if currentUserHand == 'scissors':
                return 'WIN'
            elif currentUserHand == 'rock':
                return 'LOSE'
            else:
                return 'DRAW'

        elif currentPcHand == 'scissors':
            if currentUserHand == 'rock':
                return 'WIN'
            elif currentUserHand == 'paper':
                return 'LOSE'
            else:
                return 'DRAW'