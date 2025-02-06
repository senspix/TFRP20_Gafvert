import unittest
import search_minimax as sm


class SimpleTreeNode(sm.Node):
    def __init__(self, nodes, visited_nodes = []):
        super().__init__()
        self.nodes= nodes
        self.visited_nodes = visited_nodes

    def is_terminal(self):
        return len(self.nodes['children']) == 0

    def evaluate(self):
        return self.nodes['value']

    def get_children(self):
        for node in self.nodes['children']:
            self.visited_nodes.append(node['value'])
            yield SimpleTreeNode(node,self.visited_nodes)
            
class TestMinimax(unittest.TestCase):
           
    def test_minimax_maximizing(self):
        # Test simple tree where maximizing player should choose highest value

        tree = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 5, 'children': []},
            {'value': 2, 'children': []}
        ]}

        node = SimpleTreeNode(tree)
        result = node.minimax(2, float('-inf'), float('inf'), True)
        self.assertEqual(result, 5)

    def test_minimax_minimizing(self):
        # Test simple tree where minimizing player should choose lowest value
 
        tree = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 1, 'children': []},
            {'value': 2, 'children': []}
        ]}

        node = SimpleTreeNode(tree)
        result = node.minimax(2, float('-inf'), float('inf'), False)
        self.assertEqual(result, 1)

    def test_minimax_depth_limit(self):
        # Test that search stops at specified depth
        tree = {'value': 5, 'children': [
            {'value': 3, 'children': [
                {'value': 1, 'children': []}
            ]}
        ]}
        node = SimpleTreeNode(tree)        
        result = node.minimax(1, float('-inf'), float('inf'), True)
        self.assertEqual(result, 3)

    def test_find_best_child(self):
        # Test finding best move from initial state
        game_state = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 5, 'children': []},
            {'value': 2, 'children': []}
        ]}
        
        node = SimpleTreeNode(game_state)

        (child, score) = node.find_best_child(2)
        self.assertEqual(child.nodes['value'], 5)
        self.assertEqual(score, 5)
        

    def test_alpha_beta_pruning(self):
        # Test that alpha-beta pruning works correctly
        # From: https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/

        tree = {'value': 'A', 'children': [ 
            {'value': 'B', 'children': [ 
                {'value': 'D', 'children': [
                    {'value': 3, 'children': []},
                    {'value': 5, 'children': []}
                ]}, 
                {'value': 'E', 'children': [
                    {'value': 6, 'children': []},
                    {'value': 9, 'children': []}
                ]} 
            ]}, 
            {'value': 'C', 'children': [ 
                {'value': 'F', 'children': [
                    {'value': 1, 'children': []},
                    {'value': 2, 'children': []}
                ]}, 
                {'value': 'G', 'children': [
                    {'value': 0, 'children': []},
                    {'value': -1, 'children': []}
                ]} 
            ]} 
        ]}
        
        visited_nodes = []
        node = SimpleTreeNode(tree, visited_nodes)
        result = node.minimax(3, float('-inf'), float('inf'), True)
        self.assertEqual(result, 5)
        self.assertNotEqual([9, 'G', 0, -1], visited_nodes)
        self.assertEqual(['B', 'D', 3, 5, 'E', 6, 'C', 'F', 1, 2], visited_nodes)
       

if __name__ == '__main__':
    unittest.main(verbosity = 2)    # Run the tests.



