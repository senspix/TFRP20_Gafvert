from othello import Board
import unittest
import numpy as np
import pdb;

class TestOthello(unittest.TestCase):
    def test_init(self):
        b = Board()
        self.assertEqual(b.board[3,3], 1)
        self.assertEqual(b.board[3,4], -1)
        self.assertEqual(b.board[4,3], -1)
        self.assertEqual(b.board[4,4], 1)
        self.assertEqual(b.player, -1)


    def test_repr(self):
        b = Board()
        r = repr(b).split('\n')

    def test_copy(self):
        b = Board()
        b0  = b
        b1 = b.copy()
        np.testing.assert_array_equal(b.board, b0.board)
        np.testing.assert_array_equal(b.board, b1.board)
        b.board[0,0] = 1
        np.testing.assert_array_equal(b.board, b0.board)
        np.testing.assert_raises(AssertionError,np.testing.assert_array_equal,b.board, b1.board)
        self.assertEqual(b.board.tolist(), b0.board.tolist())
        self.assertNotEqual(b.board.tolist(), b1.board.tolist())

    def test_count(self):
        b = Board()
        self.assertEqual(b.count(), (2,2,60))

    def test_evaluate(self):
        b = Board()
        b.evaluate()
        self.assertTrue(True) # just check that evaluate returns correctly  



    def test_make_move(self):
        b = Board()
        b.make_move((3,2))
        self.assertEqual(b.board[3,2], -1)
        self.assertEqual(b.board[3,3], -1)
        self.assertEqual(b.make_move((3,1)), False)


    def test_valid_moves(self):
        b = Board()
        self.assertSetEqual(set(b.valid_moves()), set([(2, 3), (3, 2), (4, 5), (5, 4)]))
      



if __name__ == '__main__':
    unittest.main(verbosity = 2)
