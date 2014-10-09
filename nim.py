"""
    Author  : John Martinsson
    Summary : An implementation of the game Nim. The computer will play a perfect
              game if possible.
"""

class Board():
    """ The board class
    """
    def __init__(self):
        self.rows = []
        self.maxSticks = 5 # this is actually the max bits
        self.defaultBoard = [7, 5, 3]

    def getGameSettings(self):
        """ Get the settings for the board by the user
        """
        data = input('| default or custom board? : ')
        while data != 'default' and data != 'custom':
            print('| Valid input: <default>, <custom>')
            data = input('| Default or custom board: ')

        if data == 'default':
            self.rows = self.defaultBoard
        if data == 'custom':
            while True:
                data = input('| Input number of sticks for row {} ({} max): '
                .format(len(self.rows), 2**self.maxSticks-1))
            
                if data == 'done':
                    break
                
                try:
                    if not int(data) > 2**self.maxSticks-1:
                        self.rows.append(int(data))
                    else:
                        print('To many sticks')
                except Exception:
                    print('| Invalid input, to end enter:<done>')

    def displayPosition(self):
        """ Display the position of the board (as sticks)
        """
        print('|-----------------------------------------------------------------------')
        
        for r in range(len(self.rows)):
            row = self.rows[r]
            s = ['|' for i in range(row)]
            s = ''.join(s)
            template = '{0:15}{1:40}{2:50}'
            s1 = '| row {} :'.format(r)
            s2 = '({} sticks)'.format(row)

            print(template.format(s1, s, s2))

        print('|-----------------------------------------------------------------------\n')

    def checkGameWon(self):
        """ Check if all sticks are taken, then the game is won.
            
            Returns
            -------
            Bool
                True if game is over, False otherwise
        """
        return sum(self.rows) == 0

    def take(self, s, r):
        """ Take s sticks from the r:th row of this board.
            
            Returns
            -------
            Bool
                True if the move is valid, otherwise False
        """
        # check enough sticks
        if(self.rows[r] >= s):
            self.rows[r] -= s
            return True
        else:
            return False

    def reverseTake(self, s, r):
        """ Reverse a move
        """
        # reverse the take
        self.rows[r] += s


def checkParity(board):
    """ Checks the parity between the number of sticks in each row. This number is
        represented as a binary string. 

        Examples
        --------
        
        Board 1
        -------
        row 0:  0111 (7 sticks)
        row 1:  0101 (5 sticks)
        row 2:  0011 (3 sticks)
        ------------------------
        Parity: 0001 (Odd)

        That is, there is an odd number of 1:s at the right most digit between each
        row, and so on. 
        
        We say that the parity is even if we get all even, that
        is, 0000 in this case, which is a kernel position in this game. 
        
        For example we could change the parity of the board in Ex.1 to even by 
        taking 1 stick from row 2, which would turn Board 1 -> Board 2

        Board 2
        -------
        row 0: 6      = 0110 (6 sticks)
        row 1: 5      = 0101 (5 sticks)
        row 2: 3      = 0011 (3 sticks)
        ------------------------
        Parity:         0000 (Even)
        """
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
    """ Check if the board has an even parity
        
        Returns
        -------
        Bool
            True if even parity, False otherwise
    """
    # if only zeroes in the parity string, we say that the parity is even
    return int(checkParity(board), 2) == 0



def computerMove(board):
    """ Perform the next computer move, will force the player into a kernel if
        possible, otherwise it will just take a stick from one of the rows.
        
        Parameters
        ----------
        board : Board()
                The board that is being played

        Returns
        -------
        Bool
            True if this move made the computer win, False otherwise
    """
    # Loop over all possible moves, make move if it turns the board into a board
    # with even parity.
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

def playerMove(board):
    """ Get and perform the next player move, will display new board position, as well
        as check if the game is over.

        Parameters
        ----------
        board : Board()
                The board that is being played

        Return
        ------
        Bool
            True if player wins with this move, False otherwise
    """
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
    """ The main game loop
    """
    # initialize the board
    board = Board()
    print('|-----------------------------------------------------------------------')
    print('| Game settings:')
    print('|                <default> : for a default board')
    print('|                <custom>  : for custom settings')
    print('|                <done>    : when done entering custom settings')
    print('|-----------------------------------------------------------------------\n')
    # get the game settings from the user
    print('|-----------------------------------------------------------------------')
    board.getGameSettings()
    print('|-----------------------------------------------------------------------\n')
    # display the board position
    print('|=======================================================================')
    print('| The game has begun!')
    print('|=======================================================================')
    print('| Moves on form  : <sticks,row>  : will take #sticks from r:th row')
    print('| Example        : <3,0>         : 3 sticks will be taken from row 0.')
    print('|')
    print('| Nim rules: http://en.wikipedia.org/wiki/Nim')
    print('|-----------------------------------------------------------------------\n')

    board.displayPosition()
    playerWon = False
    computerWon = False

    # game main loop, loop until either player or computer has won
    while not playerWon and not computerWon:
        playerWon = playerMove(board)
        computerWon = computerMove(board)

if __name__ == "__main__":
    main()
