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



if __name__ == '__main__':
    unittest.main(verbosity = 2)
