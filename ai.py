from __future__ import absolute_import, division, print_function
import copy, random
from game import Game

MOVES = {0: 'up', 1: 'left', 2: 'down', 3: 'right'}
MAX_PLAYER, CHANCE_PLAYER = 0, 1 

# Tree node. To be used to construct a game tree. 
class Node: 
    # Recommended: do not modify this __init__ function
    def __init__(self, state, player_type):
        self.state = (state[0], state[1])
        #first is tile matrix, second is score

        # to store a list of (direction, node) tuples
        self.children = []

        self.player_type = player_type

    # returns whether this is a terminal state (i.e., no children)
    def is_terminal(self):
        game = Game(*self.state)
        return game.game_over()

# AI agent. Determine the next move.
class AI:
    #AI(copy.deepcopy(self.tile_matrix), self.score)
    # Recommended: do not modify this __init__ function
    def __init__(self, root_state, search_depth=3): 
        self.root = Node(root_state, MAX_PLAYER)
        self.search_depth = search_depth
        self.simulator = Game(*root_state)

    # (Hint) Useful functions: 
    # self.simulator.current_state, self.simulator.set_state, self.simulator.move

    # TODO: build a game tree from the current node up to the given depth
    def build_tree(self, node=None, depth=0,search_depth = 3):
        if node is None:
            node = self.root
        
        if depth == self.search_depth or node.is_terminal():
            #print(f"Reached terminal or max depth at node: {node.state}")
            return
        
        if node.player_type == MAX_PLAYER:
            for move in range(4):
                self.simulator.set_state(*node.state)
                if self.simulator.move(move):
                    child_state = self.simulator.current_state()
                    child_node = Node(child_state, CHANCE_PLAYER)
                    node.children.append((move, child_node))
                    ##print(f"Added child for move {move}: {child_state}")
                    self.build_tree(child_node, depth + 1)
                else:
                    terminal_state = (node.state[0], -100)
                    child_node = Node(terminal_state, CHANCE_PLAYER)
                    node.children.append((move, child_node))
                    #print(f"Added terminal child for move {move}: {terminal_state}")
        else:
            open_tiles = self.simulator.get_open_tiles()
            if not open_tiles:
                #print("No open tiles available")
                return
            
            for (i, j) in open_tiles:
                self.simulator.set_state(*node.state)
                self.simulator.tile_matrix[i][j] = 2
                child_state = self.simulator.current_state()
                child_node = Node(child_state, MAX_PLAYER)
                node.children.append((None, child_node))
                #print(f"Added chance child at ({i}, {j}): {child_state}")
                self.build_tree(child_node, depth + 1)

    # TODO: expectimax calculation.
    # Return a (best direction, expectimax value) tuple if node is a MAX_PLAYER
    # Return a (None, expectimax value) tuple if node is a CHANCE_PLAYER
    def expectimax(self, node=None):
        if node is None:
            node = self.root
        
        if not node.children:
            return None, node.state[1]
        
        if node.player_type == MAX_PLAYER:
            best_value = float('-inf')
            best_move = None
            for move, child in node.children:
                _, value = self.expectimax(child)
                if value > best_value:
                    best_value = value
                    best_move = move
            ##print("best_move: ", best_move)
            ##print("best_value: ", best_value)
            return best_move, best_value
        else:
            total_value = 0
            for _, child in node.children:
                _, value = self.expectimax(child)
                total_value += value

            return None, total_value / len(node.children)
    def calculate_smoothness(tile_matrix):
        smoothness = 0
        for i in range(len(tile_matrix)):
            for j in range(len(tile_matrix[i]) - 1):
                smoothness -= abs(tile_matrix[i][j] - tile_matrix[i][j + 1])
                smoothness -= abs(tile_matrix[j][i] - tile_matrix[j + 1][i])
        return smoothness

    def calculate_monotonicity(tile_matrix):
        monotonicity = 0
        for row in tile_matrix:
            for i in range(len(row) - 1):
                if row[i] > row[i + 1]:
                    monotonicity += row[i] - row[i + 1]
        for col in zip(*tile_matrix):
            for i in range(len(col) - 1):
                if col[i] > col[i + 1]:
                    monotonicity += col[i] - col[i + 1]
        return monotonicity        
    def evaluate_state(self,tile_matrix, score):
        max_tile = max(max(row) for row in tile_matrix)
        empty_tiles = sum(row.count(0) for row in tile_matrix)
        smoothness = self.calculate_smoothness(tile_matrix)
        monotonicity = self.calculate_monotonicity(tile_matrix)
        return (score +
                1.0 * max_tile +
                2.0 * empty_tiles +
                0.1 * smoothness +
                1.0 * monotonicity)
    def expectimax_ec(self, node=None):
        if node is None:
            node = self.root
        
        if not node.children:
            return None, self.evaluate_state(node.state[0], node.state[1])
        
        if node.player_type == MAX_PLAYER:
            best_value = float('-inf')
            best_move = None
            for move, child in node.children:
                _, value = self.expectimax(child)
                if value > best_value:
                    best_value = value
                    best_move = move
            return best_move, best_value
        else:
            total_value = 0
            for _, child in node.children:
                _, value = self.expectimax(child)
                total_value += value
            return None, total_value / len(node.children)
    # Return decision at the root
    def compute_decision(self):
        tree = self.build_tree(self.root, 0,3)
        direction, _ = self.expectimax(self.root)
        return direction, tree

    def compute_decision_ec(self):
        self.build_tree(self.root, 0,3)
        direction, _ = self.expectimax_ec(self.root)
        return direction

