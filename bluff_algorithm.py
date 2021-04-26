import random
from pypokerengine.engine.poker_constants import PokerConstants
import pypokerengine.engine.action_checker
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards
from pypokerengine.engine.hand_evaluator import HandEvaluator
from eval_cards import eval_cards

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

    # with the estimate win rate, due to PyPokerEngine's inability to give accurate player count
    #   the function must be hand fed two values before the game (initial stack size and players)
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
            if explore == 0:
                next_action = 'fold'
            elif explore == 1 and call_amount <= 50:
                next_action = 'call'

    if amount is None:
        items = [item for item in valid_actions if item['action'] == next_action]
        amount = items[0]['amount']
    #print(next_action, amount)
    return next_action, amount