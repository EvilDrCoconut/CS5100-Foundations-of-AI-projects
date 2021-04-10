import random
from pypokerengine.engine.poker_constants import PokerConstants
import pypokerengine.engine.action_checker
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards, evaluate_hand
from pypokerengine.engine.hand_evaluator import HandEvaluator

def Poker_Bot(self):
    self.__initiate__()

    # needs to record opponents last movde
    opponents_last_move = []


    def estimate_win_rate(nb_simulation, nb_player, hole_card, community_card=None):
        if not community_card: community_card = []

        # Make lists of Card objects out of the list of cards
        community_card = gen_cards(community_card)
        hole_card = gen_cards(hole_card)

        # Estimate the win count by doing a Monte Carlo simulation
        win_count = sum([montecarlo_simulation(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
        return 1.0 * win_count / nb_simulation

    def montecarlo_simulation(nb_player, hole_card, community_card):
        # Do a Monte Carlo simulation given the current state of the game by evaluating the hands
        community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
        unused_cards = _pick_unused_card((nb_player - 1) * 2, hole_card + community_card)
        opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(nb_player - 1)]
        opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
        my_score = HandEvaluator.eval_hand(hole_card, community_card)
        return 1 if my_score >= max(opponents_score) else 0




    def bluff(score, hole, community):

        #win_rate = estimate_win_rate()

        cards = hole + community
        raise_discount = .9; all_in_discount = .2
        next_action = 'call'; amount = None

        flag = evaluate_hand(hole, community)

        '''
        if HandEvaluator.__is_straightflash(cards): score = score * 25
        if HandEvaluator.__is_fourcard(cards): score = score * 20
        if HandEvaluator.__is_fullhouse(cards): score = score * 14
        if HandEvaluator.__is_flash(cards): score = score * 10
        if HandEvaluator.__is_straight(cards): score = score * 8
        if HandEvaluator.__is_threecard(cards): score = score * 5
        if HandEvaluator.__is_twopair(cards): score = score * 3
        if HandEvaluator.__is_onepair(cards): score = score * 2
        '''

        for opp in opponents_last_move:
            if opp == PokerConstants.Action.FOLD:
                continue
            elif opp == PokerConstants.Action.CALL:
                continue
            elif opp == PokerConstants.Action.RAISE:
                score = score * raise_discount
            elif opp == PokerConstants.Action.ANTE:
                score = score * all_in_discount

        if score*raise_discount > 250:
            if score > 500:
                next_action = 'raise'
                amount =  'max'
            else:
                next_action = 'raise'
                amount = 'min'
        elif 250 > score > 100:
            next_action = 'call'
        else:
            if len(community) > 4:
                next_action = 'call'
            else:
                next_action = 'fold'
                amount = 0

        return next_action, amount
