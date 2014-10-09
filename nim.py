class Board():
    def __init__(self):
        self.rows = []
        self.maxSticks = 8

    def getGameSettings(self):
        data = input('Input number of sticks for row {} (max {}):'
        .format(len(self.rows), 2**self.maxSticks-1))
        
        # Get the input
        while data != 'end':
            if not int(data) > 2**self.maxSticks-1:
                self.rows.append(int(data))
            else:
                print('To many sticks')

            data = input('Input number of sticks for row {} (max {}):'
            .format(len(self.rows), 2**self.maxSticks-1))

    def displayPosition(self):
        for row in self.rows:
            r = ['|' for i in range(row)]
            s = ''.join(r)
            print(s + ' \t({})'.format(row))

    def checkGameWon(self):
        return sum(self.rows) == 0

    def take(self, s, r):
        # check enough sticks
        if(self.rows[r] >= s):
            self.rows[r] -= s
            return True
        else:
            return False

    def reverseTake(self, s, r):
        # reverse the take
        self.rows[r] += s

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
    return checkParity(board) == '00000000'


# Perform the next computer move, will force the player into a kernel if
# possible, otherwise it will just take a stick from one of the rows.
def computerMove(board):
    # get the parity in interger format
    for r in range(len(board.rows)):
        for i in range(board.rows[r]):
            s = i+1
            #try to take i sticks from r
            board.take(s, r)
            # The kernel position of this game is to put the opponent into a
            # position where the parity between all binary numbers are even.
            if parityEven(board):    
                print('Computer made move: {},{}'.format(s, r))

                if(board.checkGameWon()):
                    print('Computer won!')
                    board.displayPosition()
                    return True
                else:
                    board.displayPosition()
                return False
            else:
                board.reverseTake(s, r)

    # If in losing position, just take a stick.
    for r in range(len(board.rows)):
        if board.rows[r] >= 1:
            board.take(1, r)
            print('Computer made move: {},{}'.format(s, r))
            board.displayPosition()

            return False

# Get and perform the next player move, will display new board position, as well
# as check if the game is over.
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
    print('Will now ask for game settings. When done enter: \'end\'')
    print('Standard board is: row 0: 7, row 1: 5, row2: 3')
    print('-----------------------------------------------------------------------\n')
    # get the game settings from the user
    print('-----------------------------------------------------------------------')
    board.getGameSettings()
    print('-----------------------------------------------------------------------\n')
    # display the board position
    print('-----------------------------------------------------------------------')
    print('The game has begun, moves are assumed to be on form <sticks,row>')
    print('For example if you input: <3,0> then 3 sticks will be taken from row 0.')
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
