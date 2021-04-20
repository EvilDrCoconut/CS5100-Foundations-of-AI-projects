import random
import eval_cards
from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.poker_constants import PokerConstants
import pypokerengine.engine.action_checker
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards, evaluate_hand
from pypokerengine.engine.hand_evaluator import HandEvaluator
from pypokerengine.engine.game_evaluator import GameEvaluator
from pypokerengine.engine import action_checker
from pypokerengine.engine import dealer
from pypokerengine.engine import player
from pypokerengine.utils import action_utils
from pypokerengine.engine.table import Table
from pypokerengine.engine.seats import Seats
from pypokerengine.engine.player import Player
from pypokerengine.utils import card_utils
import unittest

class PokerBot(BasePokerPlayer):
    def __init__(self, startingAlg= 2):
        super().__init__()
        # Initialize bot using a random implemented algorithm if user does not select one.
        self.algID = startingAlg
        self.game_info = None
        self.hole_card = None
        self.score = 0
        self.wins = 0
        self.losses = 0

    def set_algorithm(self, algID):
        # A debug function allowing someone to set the bot's algorithm at any time.
        self.algID = algID

    def evaluation(self, player_pos, round_state):
        total_opp = 0

        current_money = round_state['seats'][player_pos]['stack']

        for i in round_state['seats']:
            if i['uuid']!=round_state['seats'][player_pos]['uuid']:
                total_opp+=i['stack']
        opponent_money = total_opp/(len(round_state['seats'])-1)
        sum = current_money-0.3*opponent_money+round_state['pot']['main']['amount']
        return sum

    def minimax(self, player_pos, current_depth, valid_actions, round_state):
        '''
        players:
        player_pos:The position of player
        depth: set it to 2
        '''
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        score = 0
        numOfPlayers = len(round_state['seats'])
        depth = numOfPlayers - 1
        for index in range(player_pos, numOfPlayers - 1):
            if index + 1 <= numOfPlayers and round_state['seats'][index + 1].is_active():
                player_pos = index + 1
                break
            elif index + 1 >= numOfPlayers:
                player_pos = 0
                break

        if depth * numOfPlayers == current_depth:
            score = self.evaluation(player_pos, round_state)
            action, amount = self.bluff(score, hole, community, valid_actions)

            return action, amount

        if current_depth % numOfPlayers == 0:
            score = float('-Inf')
            for action in valid_actions:
                max_move, result = self.minimax(player_pos, current_depth, valid_actions, round_state)
                if result > score:
                    score = result
                    move = action['action']

            return move, score

        else:
            score = float('Inf')
            for action in valid_actions:
                min_move, result = self.minimax(player_pos, current_depth, valid_actions, round_state)
                if result < score:
                    score = result
                    move = action['action']
            return move, score
    
    def expectimax(self, info_to_pass):
        play_suggestion = None; util = 0
        return play_suggestion, util
        
    def alpha_beta_pruning(self, player_pos, current_depth, valid_actions, round_state, alpha = 99999, beta = -99999):
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        numOfPlayers = len(round_state['seats'])
        depth = numOfPlayers - 1
        for index in range(player_pos, numOfPlayers - 1):
            if index + 1 <= numOfPlayers and round_state['seats'][index + 1].is_active():
                player_pos = index + 1
                break
            elif index + 1 >= numOfPlayers:
                player_pos = 0
                break
        if depth * numOfPlayers == current_depth:
            score = self.evaluation(round_state['seats'][player_pos], round_state['seats'], round_state['pot']['main'])
            print(score)
            return self.bluff(score, hole, community, valid_actions)




        if current_depth % len(round_state['seats']) == 0:
            max_value = float('-Inf')
            movement = ""
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(player_pos, current_depth, valid_actions, alpha,beta)
                if score > max_value:
                    max_value = score
                    movement = action['action']
                    if max_value > beta:
                        return movement, max_value
                    if max_value > alpha:
                        alpha = max_value
            return movement, max_value
        else:

            min_value = float('Inf')
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(player_pos, depth, current_depth, valid_actions, alpha,beta)
                if score < min_value:
                    min_value = score
                    movement = action['action']
                    if min_value < alpha:
                        return movement, min_value
                    if min_value < beta:
                        beta = min_value
            return movement, min_value

    def estimate_win_rate(self, nb_simulation, nb_player, hole_card, community_card=None):
        if not community_card: community_card = []

        # Make lists of Card objects out of the list of cards
        community_card = gen_cards(community_card)
        hole_card = gen_cards(hole_card)


        # Estimate the win count by doing a Monte Carlo simulation
        win_count = sum([self.montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
        return 1.0 * win_count / nb_simulation

    def montecarlo_simulation(self, nb_player, hole_card, community_card):
        # Do a Monte Carlo simulation given the current state of the game by evaluating the hands
        community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
        unused_cards = _pick_unused_card((nb_player - 1) * 2, hole_card + community_card)
        opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(nb_player - 1)]
        opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
        my_score = HandEvaluator.eval_hand(hole_card, community_card)
        return 1 if my_score >= max(opponents_score) else 0

    def bluff(self,score, hole, community, valid_actions):
        win_rate = self.estimate_win_rate(100, 3, hole, community)
        cards = hole + community
        next_action = 'call'; amount = None

        multiplier = eval_cards.eval_cards(cards)
        if multiplier==None:
            multiplier = 1

        score_helper = score*multiplier
        print(win_rate)
        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0
        print(call_amount)
        if score_helper * win_rate > 200:
            raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if score_helper > 250:
                next_action = 'raise'
                amount = raise_amount_options['max']
            elif score_helper > 350:
                next_action = 'raise'
                amount = raise_amount_options['min']
            else:
                next_action = 'call'
        else:
            if can_call and call_amount == 0:
                next_action = 'call'
            else:
                next_action = 'fold'

        if amount is None:
            items = [item for item in valid_actions if item['action'] == next_action]
            amount = items[0]['amount']
        print(next_action, amount)
        return next_action, amount

    def declare_action(self, valid_actions, hole_card, round_state):

        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        call_action_info = valid_actions[1]
        self.hole_card = hole_card
        player_pos = 0
        index = 0
        for player in round_state['seats']:
            if player['name'] == 'p2':
                player_pos = index
            index+=1

        # checking what round_state consists of

        #return a pair: action, amount = call_action_info["action"], call_action_info["amount"]

        if self.algID == 1:
            action, amount = self.minimax(player_pos, -1, valid_actions, round_state)
            print(action)
            return action, amount # action returned here is sent to the poker engine
        elif self.algID == 2:
            return self.alpha_beta_pruning(player_pos, -1, valid_actions, round_state)
        elif self.algID == 3:
            return self.expectimax(round_state)
        else:
            print('error check')
            return 'fold', 0

    def receive_game_start_message(self, game_info):
        self.game_info = game_info

    def receive_round_start_message(self, round_count, hole_card, opponent_state):
        pass

    def receive_street_start_message(self, street, round_state):
        #self.round_state = round_state
        pass

    def receive_game_update_message(self, new_action, round_state):
        #self.round_state = round_state
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        #self.round_state = round_state
        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)