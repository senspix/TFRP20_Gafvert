import pdb
import logging
import copy # deep copy
import numpy as np
import search_minimax as sm
import random


# https://canvas.education.lu.se/courses/33984/assignments/225768


class Board(sm.Node):
    # Representation of an Othello board and game state
    def __init__(self,
                 display_chars = {-1:'\u25CB', 0: ' ', 1: '\u25CF'},
                 highlight_chars = {-1:'\u25C6', 0: '\u25C8', 1: '\u25C7'},
                 randomize_valid_moves = True):
        self.size = 8 # board size
        # setup position: -1 = black, +1 = white
        # self.board = [[0 for _ in range(self.size)] for _ in range(self.size)] # consider using numpy array but no clear advantage for now
        self.board = np.zeros((self.size,self.size))
        self.board[3,3] = 1
        self.board[3,4] = -1
        self.board[4,3] = -1
        self.board[4,4] = 1

        self.player = -1 # black starts
        self.transcript = []
        self.turn = 1
        self.last_move = None

        # print characters for display
        #self.display_chars = {-1:'b', 0: ' ', 1: 'w'}
        # self.display_chars = {-1:'\u26AB', 0: ' ', 1: '\u26AA'} # medium circles too wide
        #self.display_chars = {-1:'\u25CF', 0: ' ', 1: '\u25CB'} # small circles of right width
        #self-highlight_chars = {-1:'\u29BF', 0: '\u2388', 1: '\u29BE'} # looks bad
        self.highlight_chars = highlight_chars
        self.display_chars = display_chars

        self.randomize_valid_moves = randomize_valid_moves

        # build static weight matrix
        # https://courses.cs.washington.edu/courses/cse573/04au/Project/mini1/RUSSIA/miniproject1_vaishu_muthu/Paper/Final_Paper.pdf
        w = np.matrix([4,-3,2,2,-4,-1,-1,1,0,1])
        tri = np.zeros((4,4))
        tri[np.triu_indices(4,0)] = w
        tri = tri + np.triu(tri,1).T
        self.weight_matrix = np.vstack([np.hstack([tri,np.fliplr(tri)]),np.flipud(np.hstack([tri,np.fliplr(tri)]))])


    def __repr__(self):
        return self.str()
    
    def print(self, highlight = []):
        # prints the board with optional highlighted squares 
        # highlight is a list of (i,j) tuples (default empty)
        # 
        print(self.str(highlight))

    def display_char(self, i, j, highlight = []):
        # returns the character for a square (i,j) with optional highlight
        if (i,j) in highlight:
            return self.highlight_chars[self.board[i,j]]
        else:
            return self.display_chars[self.board[i,j]]
        
    def str(self, highlight = []):
        # converts a board to a string
        # return '  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n' + \
        #     '\n'.join([str(i+1) + ' ' + ' '.join([self.display_char(i,j,highlight) for (j,x) in enumerate(row)]) + ' ' + str(i+1) for (i,row) in enumerate(self.board)]) + \
        #     '\n  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n'
        return '  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n' + \
            '\n'.join([str(i+1) + ' ' + ' '.join([self.display_char(i,j,highlight) for j in range(self.size)]) + ' ' + str(i+1) for i in range(self.size)]) + \
            '\n  ' + ' '.join([chr(ord('a')+i) for i in range(self.size)]) + '\n'

    def count(self):
        # returns number of black, white and empty squares
        b = w = e = 0
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i,j] == -1:
                    b += 1
                elif self.board[i,j] == 1:
                    w += 1
                else:
                    e += 1
        return (b,w,e) # black, white, empty

    def score(self):
        # returns final score of the game (negative for black, winner gets points for empty squares)
        (b, w, e) = self.count() 
        if b ==  w: # draw
            return 0
        elif b > w: # black wins
            return -b - e
        else: # white wins
            return w + e
        
    def evaluate(self):
        # returns a heuristic evaluation of the board, e.g. (weighted sum of):
        #   coin parity: difference in number of pieces for black and white
        #   mobility: difference in number of valid moves for black and white
        #   difference in number of corners for black and white
        #   difference in number of pieces in the center for black and white
        #   difference in number of pieces on the edges for black and white
        #   number of legal move
        static_b = np.sum((self.board == -1) * self.weight_matrix)
        static_w = np.sum((self.board == 1) * self.weight_matrix)
        (b,w,e) = self.count()
        return b - w if self.is_terminal() else static_b - static_w

    def is_terminal(self):
        # returns True if the game is over, False otherwise
        # the game is over if at least one of the following conditions holds true:
        #   no player has a valid move
        #   the board is full
        #   the board has pieces of only one color
        # Get valid moves for current player
        moves = self.valid_moves()
        # Store current turn
        current_turn = self.player
        # Try opponent's moves if current player has no moves
        if not moves:
            self.player = -self.player
            moves = self.valid_moves()
            self.player = current_turn
            if not moves:  # Neither player has valid moves
                return True

        # Count pieces
        b, w, e = self.count()
        # Board is full or only one color remains
        if e == 0 or b == 0 or w == 0:
            return True

        return False
    
    def get_children(self):
        # returns a list of all possible children of the current node
        # children are all possible moves for the current player
        # return pass move if no valid

        valid_moves = self.valid_moves()
        if len(valid_moves) > 0: # valid moves 
            for move in valid_moves:
                child = self.copy()
                child.make_move(move)
                yield child
        else: # pass
            child = self.copy()
            child.make_move(None) 
            yield child

    def copy(self):
        # returns a deep copy of the board
        # (brute force implementation)
        return copy.deepcopy(self)
        
    def valid_move(self, move):
        # returns True if (i,j) is a valid move for the current player
        # False otherwise
        # move is a tuple (i,j) with i=row, j=column
        # check if square is empty
        (i,j) = move
        if self.board[i][j] != 0:
            return False
        # check if move is valid in any direction
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                if di == 0 and dj == 0:
                    continue
                if self.valid_move_dir((i,j), (di,dj)):
                    return True
        return False
    
    def valid_move_dir(self, move, direction):
        # returns True if move (i,j) in direction (di,dj) is valid
        # False otherwise
        # move is a tuple (i,j) with i=row, j=column
        # direction is a tuple (di,dj) with di=row increment, dj=column increment
        # check if move is valid in direction
        # check if move is inside the board
        (i,j) = move
        (di,dj) = direction
        if not (0 <= i+di < self.size and 0 <= j+dj < self.size):
            return False
        # move must be in direction of opponent
        if self.board[i+di,j+dj] != -self.player:
            return False
        # check if there is a sequence of opponent pieces followed by a piece of the current player
        i += 2*di
        j += 2*dj
        while 0 <= i < self.size and 0 <= j < self.size:
            if self.board[i,j] == 0:
                return False
            if self.board[i,j] == self.player:
                return True
            i += di
            j += dj
        return False

    def valid_moves(self):
        # returns a list of valid moves for the current player
        valid_moves = [(i,j) for i in range(self.size) for j in range(self.size) if self.valid_move((i,j))]
        if self.randomize_valid_moves:
            random.shuffle(valid_moves)
        return valid_moves
    
    def flip_dir(self, move, direction):
        # flips pieces in direction (di,dj) starting from (i,j)
        # move is a tuple (i,j) with i=row, j=column
        # direction is a tuple (di,dj) with di=row increment, dj=column increment
        (i,j) = move
        (di,dj) = direction
        i += di
        j += dj
        while self.board[i,j] == -self.player:
            self.board[i,j] = self.player
            i += di
            j += dj

    def flip(self, move):
        # flips pieces for a move (i,j)
        # move is a tuple (i,j) with i=row, j=column
        (i,j) = move
        for di in [-1,0,1]:
            for dj in [-1,0,1]:
                if di == 0 and dj == 0:
                    continue
                if self.valid_move_dir((i,j), (di,dj)):
                    self.flip_dir((i,j), (di,dj))

    def make_move(self, move, check = True):
        # updates the board with the move (if valid)
        # returns True if move is valid, False otherwise
        # move is a tuple (i,j) with i=row, j=column
        # move == None means pass
        if move == None:
            if check and len(self.valid_moves()) > 0:
                return False
        else:
            if check and not self.valid_move(move):
                return False
            (i,j) = move
            self.board[i,j] = self.player
            self.flip(move)

        self.transcript.append((self.turn, self.player, move))
        self.last_move = move
        self.turn += 1
        self.player = -self.player
        return True

    def movestr(self, move):
        # updates the board with the move (if valid)
        # returns True if move is valid, False otherwise
        # move is a string with the move in algebraic notation 'Xn' where X is a letter 'a..h' and n a number 1..8
        return self.make_move(str2move(move))
    
    def make_pass(self):
        self.make_move(None)

    def find_random_move(self):
        valid_moves = self.valid_moves()
        if len(valid_moves) > 0:
            return random.choice(valid_moves)
        else:
            return None 
        
    def input_user_move(self):
        valid_moves = move2str(self.valid_moves())
        if len(valid_moves) > 0:
            while True:
                inp = input(f'Enter {"black" if b.player == -1 else "white"} move for turn {self.turn} {valid_moves}: ')
                if inp in valid_moves:
                    break
            return str2move(inp)
        else:
            print(f'{"Black" if b.player == -1 else "White"} pass in turn {self.turn}')
            return None

    
def move2str(move):
    # converts a of move (i,j) to algebraic notation
    if move == None:
        return 'pass'
    elif isinstance(move,tuple):
        return chr(ord('a')+move[1])+str(move[0]+1)
    elif isinstance(move,list):
        return list(map(move2str, move))



def str2move(move):
    # converts algebraic notation to a move (i,j)
    if move == '':
        return None
    elif isinstance(move,str):
        return (int(move[1])-1, ord(move[0])-ord('a'))
    elif isinstance(move,list):
        return list(map(str2move, move))
    



if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    while True: 
        inp = input("Do you want to play black ('b') or white ('w') or none ('n')? ")
        if inp in ['b','w','n']:
            break
    black_user_player = inp == 'b'
    white_user_player = inp == 'w'
    print(f'playing a game (black = {"user" if black_user_player else "computer"}, white = {"user" if white_user_player else "computer"})')
    b = Board()
    print(b)
    depth = 3
    time_limit = 1. # computer per move time limit in seconds
    while not b.is_terminal() and b.turn < 100:
        if b.player == -1: # black
            if black_user_player:
                m = b.input_user_move()
            else:
                # m = b.find_random_move()
                c = b.find_best_move(depth,True,time_limit = time_limit)
                m = None if c == None else c.last_move
        else: # white
            if white_user_player:
                m = b.input_user_move()
            else:
                # m = b.find_random_move()
                c = b.find_best_move(depth,False,time_limit=time_limit)
                m = None if c == None else c.last_move
        if m == None:
            #print(i,b.display_chars[b.player],'pass')
            b.make_move(None)
        else:    
            #print(i,b.display_chars[b.player],move2str(m.move))
            b.make_move(m)
        print(f'Turn {b.turn}: {b.display_chars[b.player]} plays {move2str(m)}')
        if black_user_player or white_user_player: 
            print(b)       


    print(b)
    (b,w,e) = b.count()
    print(f'{"Black wins" if b > w else "White wins" if w > b else "Draw"} (black:{b}, white:{w}, empty:{e})')


    