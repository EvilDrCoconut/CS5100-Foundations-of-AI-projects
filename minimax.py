from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine import action_checker
from pypokerengine.engine import dealer
from pypokerengine.engine import player
from pypokerengine.utils import action_utils
from pypokerengine.engine import table
import unittest

 def minimax(self,players, player_pos, depth, current_depth, ghostNumber, sb_amount, valid_actions):
        community = table.Table.get_community_card(self)
        hole = players[player_pos].hole_card
        current_depth += 1
        if depth * ghostNumber == current_depth:
            return self.bluff(self.score, hole, community), "Stop"
        if current_depth%ghostNumber==0:
            score = float('-Inf')
            for action in valid_actions:
                result, max_move = self.minimax(players,table.Table.next_active_player_pos(self,player_pos), depth, current_depth, ghostNumber, valid_actions)
                if result > score:
                    score = result
                    move = action
                    self.score = score
            return score, move

        else:
            score = float('Inf')
            for action in valid_actions:
                result, min_move = self.minimax(players,table.Table.next_active_player_pos(self,player_pos), depth, current_depth, ghostNumber,valid_actions)
                if result < score:
                    score = result
                    move = action
                    self.score = score
            return score, move


