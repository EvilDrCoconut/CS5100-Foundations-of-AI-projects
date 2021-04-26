from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine import action_checker
from pypokerengine.engine import dealer
from pypokerengine.engine import player
from pypokerengine.utils import action_utils
from pypokerengine.engine import table
import unittest

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
        print(next_round_state['action_histories']['preflop'][index]['amount'])
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
        for i in reversed(next_round_state['action_histories']['preflop']):
            if 'amount'not in i.keys():
                raise_amount = 15

        print(next_round_state['action_histories']['preflop'][index])
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

    if player_pos>=numOfPlayers:
        player_pos=0

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
                move = max_move

        return move, max_value

    else:
        min_value = float('Inf')
        for action in valid_actions:
            min_move, result = self.minimax(player_pos+1, current_depth, valid_actions, self.gen_next_round_state(player_pos,action,round_state))
            if result < min_value:
                min_value = result
                move = min_move

        return move, min_value
    
def alpha_beta_pruning(self, player_pos, current_depth, valid_actions, round_state, alpha, beta):
    community = round_state['community_card']
    hole = self.hole_card
    current_depth += 1
    numOfPlayers = len(round_state['seats'])
    depth = numOfPlayers - 1
    if player_pos>=numOfPlayers:
        player_pos=0
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