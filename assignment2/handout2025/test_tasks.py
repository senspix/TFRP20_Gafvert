import unittest
from tasks import *

class TestEvaluation(unittest.TestCase):
    def test_setup_grid(self):
        g = (4, 4)
        r, c = g
        sm, tm = setup_grid(g)
        self.assertEqual(sm.get_num_of_states(), r*c*4)
        self.assertEqual(sm.get_num_of_readings(), r*c+1)
        self.assertEqual(tm.get_num_of_states(), r*c*4)

if __name__ == '__main__':
    unittest.main()
