from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine import action_checker
from pypokerengine.engine import dealer
from pypokerengine.engine import player
from pypokerengine.utils import action_utils
from pypokerengine.engine import table
import unittest

class MinimaxAgent(BasePokerPlayer):
    def __init__(self):
        self.score = 0
    def manhattanDistance(xy1, xy2):
        "Returns the Manhattan distance between points xy1 and xy2"
        return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])
    def getAction(self, players, sb_amount, player_pos, player_num):
        depth = 2
        def minimax(players, player_pos, depth, current_depth, ghostNumber):
            community = table.get_community_card()
            hole = players[player_pos].hole_card
            current_depth += 1
            if depth * ghostNumber == current_depth:
                return self.bluff(self.score, hole, community), "Stop"
            if current_depth==ghostNumber or current_depth==0:
                score = float('-Inf')
                for action in action_utils.generate_legal_actions(players, player_pos, sb_amount):
                    result, max_move = minimax(players,table.next_active_player_pos(player_pos), depth, current_depth, ghostNumber)
                    if result > score:
                        score = result
                        move = action
                        self.score = score
                return score, move
            else:
                score = float('Inf')
                for action in action_utils.generate_legal_actions.legal_actions(sb_amount):
                    result, min_move = minimax(players,table.next_active_player_pos(player_pos), depth, current_depth, ghostNumber)
                    if result < score:
                        score = result
                        move = action
                        self.score = score
                return score, move

        result, action = minimax(players, player_pos, depth, -1, player_num)
        return result



