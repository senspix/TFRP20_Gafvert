import pdb

class Board():
    def __init__(self,
                 display_chars = {-1:'\u25CF', 0: ' ', 1: '\u25CB'}):
        self.size = 8 # board size
        # setup position: -1 = black, +1 = white
        self.board = [[0 for _ in range(self.size)] for _ in range(self.size)]
        self.board[3][3] = 1
        self.board[3][4] = -1
        self.board[4][3] = -1
        self.board[4][4] = 1
        # self.board[0][0] = 1
        # self.board[0][-1] = -1
        # self.board[-1][0] = -1
        # self.board[-1][-1] = 1
        self.turn = -1 # black starts
        # print characters for display
        #self.display_chars = {-1:'b', 0: ' ', 1: 'w'}
        # self.display_chars = {-1:'\u26AB', 0: ' ', 1: '\u26AA'} # medium circles too wide
        #self.display_chars = {-1:'\u25CF', 0: ' ', 1: '\u25CB'} # small circles of right width
        self.display_chars = display_chars

    def __repr__(self):
#        return '  '+' '.join([chr(ord('a')+i) for i in range(self.size)])+'\n'+'\n'.join([str(i+1)+' '+ ' '.join([self.display_chars[x] for x in row]) for (i,row) in enumerate(self.board)])
        return '  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n' + \
            '\n'.join([str(i+1) + ' ' + ' '.join([self.display_chars[x] for x in row]) + ' ' + str(i+1) for (i,row) in enumerate(self.board)]) + \
            '\n  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n'

    def score():
        pass



    