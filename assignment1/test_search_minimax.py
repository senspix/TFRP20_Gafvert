import unittest
import search_minimax

class TestMinimax(unittest.TestCase):
    def test_minimax_maximizing(self):
        # Test simple tree where maximizing player should choose highest value
        node = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 5, 'children': []},
            {'value': 2, 'children': []}
        ]}
        
        def mock_get_children(n):
            return n['children']
            
        def mock_evaluate(n):
            return n['value']
            
        def mock_is_terminal(n):
            return len(n['children']) == 0
            
        search_minimax.get_children = mock_get_children
        search_minimax.evaluate = mock_evaluate 
        search_minimax.is_terminal = mock_is_terminal
        
        result = search_minimax.minimax(node, 2, float('-inf'), float('inf'), True)
        self.assertEqual(result, 5)

    def test_minimax_minimizing(self):
        # Test simple tree where minimizing player should choose lowest value
        node = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 1, 'children': []},
            {'value': 2, 'children': []}
        ]}
        
        def mock_get_children(n):
            return n['children']
            
        def mock_evaluate(n):
            return n['value']
            
        def mock_is_terminal(n):
            return len(n['children']) == 0
            
        search_minimax.get_children = mock_get_children
        search_minimax.evaluate = mock_evaluate
        search_minimax.is_terminal = mock_is_terminal
        
        result = search_minimax.minimax(node, 2, float('-inf'), float('inf'), False)
        self.assertEqual(result, 1)

    def test_minimax_depth_limit(self):
        # Test that search stops at specified depth
        node = {'value': 5, 'children': [
            {'value': 3, 'children': [
                {'value': 1, 'children': []}
            ]}
        ]}
        
        def mock_get_children(n):
            return n['children']
            
        def mock_evaluate(n):
            return n['value']
            
        def mock_is_terminal(n):
            return len(n['children']) == 0
            
        search_minimax.get_children = mock_get_children
        search_minimax.evaluate = mock_evaluate
        search_minimax.is_terminal = mock_is_terminal
        
        result = search_minimax.minimax(node, 1, float('-inf'), float('inf'), True)
        self.assertEqual(result, 3)

    def test_find_best_move(self):
        # Test finding best move from initial state
        game_state = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 5, 'children': []},
            {'value': 2, 'children': []}
        ]}
        
        def mock_get_children(n):
            return n['children']
            
        def mock_evaluate(n):
            return n['value']
            
        def mock_is_terminal(n):
            return len(n['children']) == 0
            
        search_minimax.get_children = mock_get_children
        search_minimax.evaluate = mock_evaluate
        search_minimax.is_terminal = mock_is_terminal
        
        best_move = search_minimax.find_best_move(game_state, 2)
        self.assertEqual(best_move['value'], 5)

    def test_alpha_beta_pruning(self):
        # Test that alpha-beta pruning works correctly
        node = {'value': 0, 'children': [
            {'value': 3, 'children': []},
            {'value': 5, 'children': []},
            {'value': 2, 'children': []}  # This branch should be pruned
        ]}
        
        visited_nodes = []
        
        def mock_get_children(n):
            visited_nodes.append(n['value'])
            return n['children']
            
        def mock_evaluate(n):
            return n['value']
            
        def mock_is_terminal(n):
            return len(n['children']) == 0
            
        search_minimax.get_children = mock_get_children
        search_minimax.evaluate = mock_evaluate
        search_minimax.is_terminal = mock_is_terminal
        
        result = search_minimax.minimax(node, 2, float('-inf'), float('inf'), True)
        self.assertEqual(result, 5)
        self.assertNotIn(2, visited_nodes)

if __name__ == '__main__':
    unittest.main(verbosity=2)

if __name__ == '__main__':
    unittest.main(verbosity = 2)    # Run the tests.



