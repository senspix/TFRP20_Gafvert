# Implementation of the minimax algorithm with alpha-beta pruning.
import time

class Node:
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
    
    def minimax(self, depth, alpha, beta, maximizing_player):
        """
        Minimax algorithm with alpha-beta pruning.
        
        Args:
            node: Current game state
            depth: Maximum depth to search
            alpha: Alpha value for pruning
            beta: Beta value for pruning
            maximizing_player: Boolean indicating if current player is maximizing
        
        Returns:
            best_score: The best possible score from the current position
        """
        # Base case: if we reach maximum depth or game is over or time expired

        if depth == 0 or self.is_terminal() or time.time() - self.time_start > self.time_limit:
            return self.evaluate()

        if maximizing_player:
            best_score = float('-inf')
            for child in self.get_children():
                score = child.minimax(depth - 1, alpha, beta, False)
                best_score = max(score, best_score)
                alpha = max(alpha, best_score)
                if best_score >= beta:
                    break  # Beta cut-off
            return best_score # issue: if not terminal but no children (pass) then returns inf... should return eval?
        
        else: # minimizing player
            best_score = float('inf')
            for child in self.get_children():
                score = child.minimax(depth - 1, alpha, beta, True)
                best_score = min(score, best_score)
                beta = min(beta, best_score)
                if best_score <= alpha:
                    break  # Alpha cut-off
            return best_score
        


    # example usage
    def find_best_move(self, depth, maximizing_player=True, time_limit = float('inf')):
        best_score = float('-inf') if maximizing_player else float('inf') 
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        self.time_limit = time_limit
        self.time_start = time.time()
        
        for move in self.get_children():
            score = move.minimax(depth - 1, alpha, beta, not maximizing_player)
            if (maximizing_player and (score > best_score)) or (not maximizing_player and (score < best_score)): 
                best_score = score
                best_move = move

        # print(f'best score: {best_score} ({maximizing_player =})')
        return best_move
    
