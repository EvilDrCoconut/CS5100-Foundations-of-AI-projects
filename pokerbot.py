import random
from random import choices
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

    # Note for users, to change algorithms when init a bot:
    #   0 = fishPlayerAlgo, 1 = minimax, 2 = alpha-beta, 3 = expectimax, 4 = bluff algorithm
    def __init__(self, startingAlg = 0):
        super().__init__()
        # Initialize bot using a standard fish player algorithm unless told not to.
        self.algID = startingAlg
        self.game_info = None
        self.hole_card = None
        self.score = 0
        self.wins = 0
        self.losses = 0

        #self.whatAlgo()

    def set_algorithm(self, algID):
        # A debug function allowing someone to set the bot's algorithm at any time.
        self.algID = algID
        self.whatAlgo()


    def whatAlgo(self):
        if self.algID == 0:
            print('Fish Player Algorithm')
        elif self.algID == 1:
            print('Minimax Algorithm')
        elif self.algID == 2:
            print('Alpha-Beta Algorithm')
        elif self.algID == 3:
            print('Expectimax Algorithm')
        else:
            print('BLuff Algorithm')

    def fishPlayerAlgorithm(self, valid_actions, hole_card, round_state):
                # Estimate the win rate
        win_rate = self.estimate_win_rate(100, 2, hole_card, round_state['community_card'])

        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        amount = None

        # If the win rate is large enough, then raise
        if win_rate > 0.5:
            raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if win_rate > 0.85:
                # If it is extremely likely to win, then raise as much as possible
                action = 'raise'
                amount = raise_amount_options['max']
            elif win_rate > 0.75:
                # If it is likely to win, then raise by the minimum amount possible
                action = 'raise'
                amount = raise_amount_options['min']
            else:
                # If there is a chance to win, then call
                action = 'call'
        else:
            action = 'call' if can_call and call_amount == 0 else 'fold'

        # Set the amount
        if amount is None:
            items = [item for item in valid_actions if item['action'] == action]
            amount = items[0]['amount']



    def evaluation(self, player_pos, round_state):
        total_opp = 0

        current_money = round_state['seats'][player_pos]['stack']

        for i in round_state['seats']:
            if i['uuid']!=round_state['seats'][player_pos]['uuid']:
                total_opp+=i['stack']
        opponent_money = total_opp/(len(round_state['seats'])-1)
        sum = current_money-0.3*opponent_money+round_state['pot']['main']['amount']
        return sum

    def gen_next_round_state(self,player_pos,action,round_state):
        next_round_state = round_state
        if action=="fold":
            #print('fold')
            return next_round_state
        elif action=="call":
            #print('call')
            call_amount = 0
            index = len(next_round_state['action_histories']['preflop'])-1
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
            #print(next_round_state['action_histories']['preflop'][index])
            #call_amount = next_round_state['action_histories']['preflop'][index]['amount']
=======
            print(next_round_state['action_histories']['preflop'][index]['amount'])
>>>>>>> bbfdfcfd8976835d086c61f57ce0d7fb592bdc75
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
            for i in reversed(next_round_state['action_histories']['preflop']):
                if 'amount'not in i.keys():
                    call_amount = 15
            next_round_state['pot']['main']['amount']+=call_amount
            next_round_state['seats'][player_pos]['stack']-=call_amount
            next_round_state['action_histories'][index+1] = {'action': 'CALL', 'amount': call_amount,  'uuid': next_round_state['seats'][player_pos]['uuid']}
            return next_round_state
        else:
            #print('raise')
            raise_amount = 0
            index = len(next_round_state['action_histories']['preflop']) - 1
<<<<<<< HEAD
            #print(next_round_state['action_histories']['preflop'][index])
            #raise_amount = 1.1*next_round_state['action_histories']['preflop'][index]['amount']
            for i in reversed(next_round_state['action_histories']['preflop']):
                if 'amount'not in i.keys():
                    raise_amount = 15
=======
            for i in reversed(next_round_state['action_histories']['preflop']):
                if 'amount'not in i.keys():
                    raise_amount = 15
<<<<<<< HEAD
=======

            print(next_round_state['action_histories']['preflop'][index])
>>>>>>> bbfdfcfd8976835d086c61f57ce0d7fb592bdc75
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
            next_round_state['pot']['main']['amount'] += raise_amount
            next_round_state['seats'][player_pos]['stack'] -= raise_amount
            next_round_state['action_histories'][index + 1] = {'action': 'RAISE', 'amount': raise_amount,
                                                               'uuid': next_round_state['seats'][player_pos]['uuid']}
            return next_round_state

    def minimax(self, player_pos, current_depth, valid_actions, round_state):
        '''
        players:
        player_pos:The position of player
        depth: set it to 2
        '''
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        numOfPlayers = len(round_state['seats'])
        depth = numOfPlayers-1
<<<<<<< HEAD
        call_amount = 0
        for i in reversed(round_state['action_histories']['preflop']):
            if 'amount' in i.keys():
                call_amount = i['amount']
            else:
                call_amount = 15
        if player_pos>=numOfPlayers:
            player_pos=0
=======

        if player_pos>=numOfPlayers:
            player_pos=0

<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
=======
>>>>>>> 45d1ddc353cf8078fb153231c1ba1a0dc7dac433
        if depth * numOfPlayers == current_depth:
            #print('done')

            score = self.evaluation(player_pos, round_state)
            action, amount = self.bluff(score, hole, community, valid_actions)
            return action, amount
        move = ''
        if current_depth % len(round_state['seats']) == 0:
            max_value = float('-Inf')
            for action in valid_actions:
                max_move, result = self.minimax(player_pos+1, current_depth, valid_actions, self.gen_next_round_state(player_pos,action['action'],round_state))
                if result > max_value:
                    max_value = result
                    move = action['action']

            if move=='call':
                max_value = call_amount
            return move, max_value

        else:
            min_value = float('Inf')
            for action in valid_actions:
                min_move, result = self.minimax(player_pos+1, current_depth, valid_actions, self.gen_next_round_state(player_pos,action,round_state))
                if result < min_value:
                    min_value = result
                    move = action['action']
            if move=='call':
                min_value = call_amount
            return move, min_value
    
    def expectimax(self, info_to_pass):
        play_suggestion = None; util = 0
        return play_suggestion, util
        
    def alpha_beta_pruning(self, player_pos, current_depth, valid_actions, round_state, alpha, beta):
        community = round_state['community_card']
        hole = self.hole_card
        current_depth += 1
        numOfPlayers = len(round_state['seats'])
        depth = numOfPlayers - 1
<<<<<<< HEAD
        
        if player_pos>=numOfPlayers:
            player_pos=0
        
=======
        if player_pos>=numOfPlayers:
            player_pos=0
>>>>>>> bbfdfcfd8976835d086c61f57ce0d7fb592bdc75
        if depth * numOfPlayers == current_depth:
            score = self.evaluation(player_pos, round_state)
            action, amount = self.bluff(score, hole, community, valid_actions)
            return action, amount

        if current_depth % len(round_state['seats']) == 0:
            max_value = float('-Inf')
            movement = ""
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(player_pos+1, current_depth, valid_actions, self.gen_next_round_state(player_pos,action,round_state), alpha,beta)
                if score > max_value:
                    max_value = score
                    movement = move
                    if max_value > beta:
                        return movement, max_value
                    if max_value > alpha:
                        alpha = max_value
            return movement, max_value
        else:

            min_value = float('Inf')
            for action in valid_actions:
                move,score = self.alpha_beta_pruning(player_pos+1, current_depth, valid_actions,self.gen_next_round_state(player_pos,action,round_state), alpha,beta)
                if score < min_value:
                    min_value = score
                    movement = move
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

    def bluff(self, score, hole, community, valid_actions, bluffAlgoMain = 0):

        if bluffAlgoMain == 1 and score == -999999:
            score = eval_cards.selfScorer(hole)


        win_rate = self.estimate_win_rate(10000, 5, hole, community)
        cards = hole + community
        next_action = 'call'; amount = None

        multiplier = eval_cards.eval_cards(cards)
        if multiplier==None:
            multiplier = 1

        score_helper = score*multiplier
        # Check whether it is possible to call
        can_call = len([item for item in valid_actions if item['action'] == 'call']) > 0
        if can_call:
            # If so, compute the amount that needs to be called
            call_amount = [item for item in valid_actions if item['action'] == 'call'][0]['amount']
        else:
            call_amount = 0

        #print(win_rate, call_amount)

        # tried different raise amount thresholds, doing different raise amounts at different thresholds yielded more stable results
        #      however, the overall score was notably lower rather than going max or min
        if score_helper * win_rate > 200:
            raise_amount_options = [item for item in valid_actions if item['action'] == 'raise'][0]['amount']
            if score_helper > 650:
                next_action = 'raise'
                amount = raise_amount_options['max']
            elif score_helper > 450:
                next_action = 'raise'
                amount = raise_amount_options['min']
            else:
                next_action = 'call'
        else:
            if can_call and call_amount == 0:
                next_action = 'call'
            else:
                explore = choices([0,1], [.6, .4])
                #print(explore)
                if explore == 0:
                    next_action = 'fold'
                elif explore == 1 and call_amount <= 50:
                    next_action = 'call'

        if amount is None:
            items = [item for item in valid_actions if item['action'] == next_action]
            amount = items[0]['amount']
        #print(next_action, amount)
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

        if self.algID == 0:
            self.fishPlayerAlgorithm(valid_actions, hole_card, round_state)
        elif self.algID == 1:
            action, amount = self.minimax(player_pos, -1, valid_actions, round_state)
            print(action,amount)
            return action, amount # action returned here is sent to the poker engine
        elif self.algID == 2:
            return self.alpha_beta_pruning(player_pos, -1, valid_actions, round_state, 99999, -99999)
        elif self.algID == 3:
            return self.expectimax(round_state)
        else:
            return self.bluff(-999999, hole_card, round_state['community_card'], valid_actions, 1)

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