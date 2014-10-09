class Board():
    def __init__(self):
        self.rows = []
        self.maxSticks = 8 # this is actually the max bits

    # Get the game settings by the user
    def getGameSettings(self):
        while True:
            data = input('Input number of sticks for row {} ({} max): '
            .format(len(self.rows), 2**self.maxSticks-1))
        
            if data == 'done':
                break
            
            try:
                if not int(data) > 2**self.maxSticks-1:
                    self.rows.append(int(data))
                else:
                    print('To many sticks')
            except Exception:
                print('Invalid input, to end enter:<done>')

    # display the position of this board (as sticks)
    def displayPosition(self):
        for row in self.rows:
            r = ['|' for i in range(row)]
            s = ''.join(r)
            print(s + ' \t({})'.format(row))

    # if all sticks are taken, the game is over, and the last player that made a
    # move has won.
    def checkGameWon(self):
        return sum(self.rows) == 0

    # simply take s sticks from the r:th row of this board
    def take(self, s, r):
        # check enough sticks
        if(self.rows[r] >= s):
            self.rows[r] -= s
            return True
        else:
            return False

    # reverse a previous take move
    def reverseTake(self, s, r):
        # reverse the take
        self.rows[r] += s

# Checks the parity between the number of sticks in each row. This number is
# represented as a binary string. 
#
# For example:
# row 0: 7      = 1101
# row 1: 5      = 0101
# row 2: 3      = 0011
# ------------------------
# Parity:         OEOO
# In Binary:      1011
# O = Odd
# E = Even
#
# That is, there is an odd number of 1:s at the right most digit between each
# row, and so on. We say that the parity is even if we get all even, that is
# EEEE, or 0000, which is a kernel position in this game.
def checkParity(board):
    # initialize to parity 0
    parity = [0 for i in range(board.maxSticks)]
    for row in board.rows:
        # binary representation of row
        form = '{' + '0:0{}b'.format(board.maxSticks) + '}'
        b = form.format(row)
        for i in range(board.maxSticks):
            parity[i] += int(b[i])

    s = []
    for p in parity:
        if p%2 == 0:
            s.append('0')
        else:
            s.append('1')

    return ''.join(s)

def parityEven(board):
    # if only zeroes in the parity string, we say that the parity is even
    return int(checkParity(board), 2) == 0


# Perform the next computer move, will force the player into a kernel if
# possible, otherwise it will just take a stick from one of the rows.
# @return: Boolean Flag, if True this move made the computer win, o/w False.
def computerMove(board):
    # get the parity in interger format
    for r in range(len(board.rows)):
        for i in range(board.rows[r]):
            s = i+1
            # try the move to take i sticks from r
            board.take(s, r)
            # The kernel position of this game is to put the opponent into a
            # position where the parity between all binary numbers are even. So
            # we check if this move leads to an even parity.
            if parityEven(board):    
                print('Computer made move: {},{}'.format(s, r))

                if(board.checkGameWon()):
                    print('Computer won!')
                    board.displayPosition()
                    return True
                else:
                    board.displayPosition()
                return False
            # if not, simply reverse the move, and try the next one.
            else:
                board.reverseTake(s, r)

    # If the computer is in fact in a losing position, that is, the parity is
    # allready even, just take a stick, and be done with it.
    for r in range(len(board.rows)):
        if board.rows[r] >= 1:
            board.take(1, r)
            print('Computer made move: {},{}'.format(s, r))
            board.displayPosition()

            return False

# Get and perform the next player move, will display new board position, as well
# as check if the game is over.
# @return: Boolean Flag, if True this move made the player win, o/w False.
def playerMove(board):
    # assumed form, (sticks,row)
    while True:
        try:
            playerMove = input('Enter next move: ') 
            m = playerMove.split(',')
            s = int(m[0])
            r = int(m[1])

            if r < len(board.rows) and s <= board.rows[r]:
                board.take(s, r)
                break
            else:
                print('Invalid move')

        except Exception:
            print('Invalid input, try again. Valid input:<sticks,row>')
   
    if(board.checkGameWon()):
        print('Player won!')
        board.displayPosition()
        return True
    else:
        board.displayPosition()
        return False

def main():
    # initialize the board
    board = Board()
    print('-----------------------------------------------------------------------')
    print('Will now ask for game settings. When done enter:<done>')
    print('Standard board is: row 0: 7, row 1: 5, row 2: 3')
    print('-----------------------------------------------------------------------\n')
    # get the game settings from the user
    print('-----------------------------------------------------------------------')
    board.getGameSettings()
    print('-----------------------------------------------------------------------\n')
    # display the board position
    print('-----------------------------------------------------------------------')
    print('| The game has begun, moves are assumed to be on form <sticks,row>')
    print('| For example if you input: <3,0> then 3 sticks will be taken from row 0.')
    print('|')
    print('| Nim rules: http://en.wikipedia.org/wiki/Nim')
    print('-----------------------------------------------------------------------\n')

    board.displayPosition()
    playerWon = False
    computerWon = False

    # game main loop, loop until either player or computer has won
    while not playerWon and not computerWon:
        playerWon = playerMove(board)
        computerWon = computerMove(board)

if __name__ == "__main__":
    main()
