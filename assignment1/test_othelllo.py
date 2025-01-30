from othello import Board
import unittest
import numpy as np
import pdb;

class TestOthello(unittest.TestCase):
    def test_init(self):
        b = Board()
        self.assertEqual(b.board[3][3], 1)
        self.assertEqual(b.board[3][4], -1)
        self.assertEqual(b.board[4][3], -1)
        self.assertEqual(b.board[4][4], 1)
        self.assertEqual(b.turn, -1)


    def test_repr(self):
        b = Board()
        r = repr(b).split('\n')

    def test_copy(self):
        b = Board()
        b0  = b
        b1 = b.copy()
        self.assertEqual(b.board, b0.board)
        self.assertEqual(b.board, b1.board)
        b.board[0][0] = 1
        self.assertEqual(b.board, b0.board)
        self.assertNotEqual(b.board, b1.board)

    def test_count(self):
        b = Board()
        self.assertEqual(b.count(), (2,2,60))

    def test_score(self):
        b = Board()
        self.assertEqual(b.score(), 0)
        # add test for non-zero score when move() implemented

    def test_move(self):
        b = Board()
        b.move((3,2))
        self.assertEqual(b.board[3][2], -1)
        self.assertEqual(b.board[3][3], -1)
        b.move((3,1))
        self.assertEqual(b.board[3][1], -1)
        self.assertEqual(b.board[3][2], -1)
        self.assertEqual(b.board[3][3], -1)
        

    def test_valid_moves(self):
        b = Board()
        self.assertEqual(b.valid_moves(), [(2, 4), (3, 5), (4, 2), (5, 3)])
      



if __name__ == '__main__':
    unittest.main(verbosity = 2)
