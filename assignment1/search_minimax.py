# Implementation of the minimax algorithm with alpha-beta pruning.
import time

class Node:
    """
    Abstract base class for game tree for minimax search.
    Implementation of minimax seach with alpha-beta pruning is provided
    """

    def __init__(self):
        pass

    def is_terminal(self):
        """
        Check if the current node is a terminal state.
        Implement game-specific logic here.
        """
        raise NotImplementedError

    def evaluate(self):
        """
        Evaluate the current game state from the perspective of the max player.
        Must return Utility game score at terminal state.
        For all non terminal states s, return a heuristic evaluation Eval(s) of the board such that 
        Utility(loss) <= Eval(s) <= Utility(win) for all non terminal states s.
        Implement game-specific evaluation function here.
        """
        raise NotImplementedError

    def get_children(self):
        """
        Generate all possible moves from current state.
        Implement game-specific move generation here.
        """
        raise NotImplementedError
    
    def minimax(self, depth, alpha, beta, maximizing_player, timer_start = 0, timer_limit = float('inf')):
        """
        Minimax algorithm with alpha-beta pruning and optional timer interruption.
        
        Args:
            depth: Maximum depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Boolean indicating if current player is maximizing
            timer_start, timer_limit: search interrupted when current time exceeds timer_start + timer_limit
        
        Returns:
            best_score: The best possible score from the current position
        """
        # Base case: if we reach maximum depth or game is over or time expired

        if depth == 0 or self.is_terminal() or time.time() - timer_start > timer_limit:
            return self.evaluate()

        if maximizing_player:
            best_score = float('-inf')
            for child in self.get_children():
                score = child.minimax(depth - 1, alpha, beta, False, timer_start, timer_limit)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break  # Beta cut-off
            return best_score 
        
        else: # minimizing player
            best_score = float('inf')
            for child in self.get_children():
                score = child.minimax(depth - 1, alpha, beta, True, timer_start, timer_limit)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break  # Alpha cut-off
            return best_score
        

    def find_best_child(self, depth, maximizing_player=True, timer_limit = float('inf')):
        """
        Convenience method to initiate search from current game state using
        Minimax algorithm with alpha-beta pruning and optional timer interruption.
        
        Args:
            depth: Maximum depth to search (must be > 0)
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Boolean indicating if current player is maximizing
            timer_limit: search interrupted when time lapsed from calling this method exceeds timer_limit
        
        Returns:
            best_child: The best possible child found from the current node
                None if no children exists from current game state 
            best_score: The best possible score found from the current node
                -inf for maximizing player or +inf for minimizing player if no children exists from current game state  
        """
        if depth <= 0:
            raise ValueError("depth must be > 0")
        best_score = float('-inf') if maximizing_player else float('inf') 
        best_child = None
        alpha = float('-inf')
        beta = float('inf')
        timer_start = time.time()
        
        for child in self.get_children():
            score = child.minimax(depth - 1, alpha, beta, not maximizing_player, timer_start, timer_limit)
            if (maximizing_player and (score > best_score)) or (not maximizing_player and (score < best_score)): 
                best_score = score
                best_child = child

        return best_child, best_score
    
