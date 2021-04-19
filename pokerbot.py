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
    def __init__(self, startingAlg=-1):
        super().__init__()
        # Initialize bot using a random implemented algorithm if user does not select one.
        self.algID = startingAlg
        if startingAlg == -1:
            self.algID = random.randint(0, 3)

        #self.valid_actions = {'call':1, 'raise':2, 'fold':3}
        self.score = 0
        self.wins = 0
        self.losses = 0

        '''
        self.tb = Table()
        self.game_eval = GameEvaluator()
        self.player1 = Player(1, 1000, "Andy")
        self.player2 = Player(2, 1000, "Rowbie")
        self.player3 = Player(3, 1000, "Luke")
        self.tb.seats.sitdown(self.player1)
        self.tb.seats.sitdown(self.player2)
        self.tb.seats.sitdown(self.player3)
        self.pot = GameEvaluator.create_pot(self.tb.seats.players)[0]
        '''

    def set_algorithm(self, algID):
        # A debug function allowing someone to set the bot's algorithm at any time.
        self.algID = algID



    '''
    def run_algorithm(self, info_to_pass):
        if self.algID == 0:
            play_suggestion, util = self.minimax(info_to_pass)
        elif self.algID == 1:
            play_suggestion, util = self.expectimax(info_to_pass)
        elif self.algID == 2:
            play_suggestion, util = self.mdp(info_to_pass)
        elif self.algID == 3:
            play_suggestion, util = self.alphaBeta(info_to_pass)

        #self.bluff(play_suggestion, util)
    '''

    def evaluation(self, player, table, pot):
        total = 0
        paid_sum = player.paid_sum()
        initial_stack = player.stack
        current_money = initial_stack - paid_sum

        for i in table.seats.players:
            current = i.stack-i.paid_sum()
            total+=current
        opponent_money = total/len(table.seats.players)
        sum = current_money-0.6*opponent_money+pot
        return sum

    # def minimax(self, info_to_pass):
    def minimax(self, player_pos, current_depth, valid_actions, round_state, sb_amount):
        '''
        players:
        player_pos:The position of player
        depth: set it to 2
        '''
        table = round_state['table']
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        score = 0
        depth = len(table.seats.players) - 1

        if depth * len(table.seats.players) == current_depth:
            # return self.bluff(score, hole, community), score
            score = self.evaluation(table.seats.players[player_pos], table, round_state['main pot'])
            print(score)
            return self.bluff(score, hole, community, valid_actions)
        if current_depth % len(table.seats.players) == 0:
            score = float('-Inf')
            for action in valid_actions:
                max_move, result = self.minimax(table.next_active_player_pos(player_pos),
                                                current_depth, valid_actions, round_state, sb_amount)
                if result > score:
                    score = result
                    move = action

            # move = self.bluff(score, hole, community)
            return move, score

        else:
            score = float('Inf')
            for action in valid_actions:
                min_move, result = self.minimax(table.next_active_player_pos(player_pos),
                                                current_depth, valid_actions, round_state, sb_amount)
                if result < score:
                    score = result
                    move = action
            # move = self.bluff(score, hole, community)
            return move, score
    
    def expectimax(self, info_to_pass):
        play_suggestion = None; util = 0
        return play_suggestion, util
    '''
    def mdp(self, info_to_pass):
        play_suggestion = None; util = 0
        return play_suggestion, util
    '''
    def alpha_beta_pruning(self, player_pos, current_depth, valid_actions, round_state, sb_amount = 0, alpha = 99999, beta = -99999):
        table = round_state['table']
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        depth = len(table.seats.players) - 1

        if depth * len(table.seats.players) == current_depth:

            score = self.evaluation(table.seats.players[player_pos], table, round_state['round_state'])
            print(score)
            return self.bluff(score, hole, community, valid_actions)

        if current_depth % len(table.seats.players) == 0:
            max_value = float('-Inf')
            movement = ""
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(table.next_active_player_pos(player_pos), current_depth, valid_actions, sb_amount, alpha,beta)
                if score > max_value:
                    max_value = score
                    movement = action
                    if max_value > beta:
                        return movement, max_value
                    if max_value > alpha:
                        alpha = max_value
            return movement, max_value
        else:

            min_value = float('Inf')
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(table.next_active_player_pos(player_pos), depth, current_depth, valid_actions,sb_amount, alpha,beta)
                if score < min_value:
                    min_value = score
                    movement = action
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
        win_count = sum([card_utils._montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
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
        #raise_discount = .9; all_in_discount = .2
        next_action = 'call'; amount = None

        multiplier = eval_cards.eval_cards(cards)
        if multiplier==None:
            multiplier = 1
        print(multiplier)
        score_helper = score*multiplier

        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        if score_helper * win_rate > 250:
            raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if score_helper > 450:
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

        return next_action, amount

    
    def declare_action(self, valid_actions, hole_card, round_state):
        # a valid action is a dictionary (tuple?) of the form {'action': 'fold', 'amount': 2}
        # needs both action name (fold, call, raise) and an amount

        # hole card is a length 2 list of the two cards (strings like 'DA', 'SK')
        
        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        call_action_info = valid_actions[1]
        print(round_state)
        #action, amount = call_action_info["action"], call_action_info["amount"]
        return self.alpha_beta_pruning(0, 2, -1, valid_actions, round_state, 100)
        #return self.minimax(0, -1,valid_actions, 100, round_state['table'])  # action returned here is sent to the poker engine

    def receive_game_start_message(self, game_info):
        self.game_info = game_info
        # choose an algorithm??

    def receive_round_start_message(self, round_count, hole_card, opponent_state):
        # changed name of seats to opponent state. May need to change back if this causes an issue
        self.round_count = round_count
        self.hole_card = hole_card
        self.opponent_state = opponent_state

    def receive_street_start_message(self, street, round_state):
        self.street = street
        self.round_state = round_state

    def receive_game_update_message(self, new_action, round_state):
        self.new_action = new_action
        self.round_state = round_state

    def receive_round_result_message(self, winners, hand_info, round_state):
        self.winners = winners
        self.opponent_hand = hand_info
        self.round_state = round_state

        is_winner = self.uuid in [item['uuid'] for item in winners]
        self.wins += int(is_winner)
        self.losses += int(not is_winner)