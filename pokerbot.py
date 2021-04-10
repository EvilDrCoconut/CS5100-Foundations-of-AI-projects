import random
from pypokerengine.players import BasePokerPlayer
from pypokerengine.engine.poker_constants import PokerConstants
import pypokerengine.engine.action_checker
from pypokerengine.utils.card_utils import _pick_unused_card, _fill_community_card, gen_cards
from pypokerengine.engine.hand_evaluator import HandEvaluator

class PokerBot(BasePokerPlayer):
    def __init__(self, startingAlg=-1):
        # Initialize bot using a random implemented algorithm if user does not select one.
        self.algID = startingAlg
        if startingAlg == -1:
            self.algID = random.randint(0, 3)

        self.valid_actions = {}
        self.game_info = {}
        self.hole_card = []
        self.round_state = {}
        self.round_count = 0
        self.opponent_state = {}
        self.street = ""
        self.new_action = {} # new action is the same as a valid action with a user id in front position
        self.winners = {} # similar to an entry in opponent_state but with bot itself as a possiblity
        self.opponent_hand = []


    def set_algorithm(self, algID):
        # A debug function allowing someone to set the bot's algorithm at any time.
        self.algID = algID



    def run_algorithm(self, info_to_pass):
        if self.algID == 0:
            play_suggestion, util = self.minimax(info_to_pass)
        elif self.algID == 1:
            play_suggestion, util = self.expectimax(info_to_pass)
        elif self.algID == 2:
            play_suggestion, util = self.mdp(info_to_pass)
        elif self.algID == 3:
            play_suggestion, util = self.alphaBeta(info_to_pass)

        self.bluff(play_suggestion, util)

    def minimax(self, info_to_pass):
        # Four algorithm implementations go here.
        # Return expected value of return to pass to bluff
        play_suggestion = None
        return play_suggestion, util
    def expectimax(self, info_to_pass):
        play_suggestion = None
        return play_suggestion, util
    def mdp(self, info_to_pass):
        play_suggestion = None
        return play_suggestion, util
    def alphaBeta(self, info_to_pass):
        play_suggestion = None
        return play_suggestion, util

    def estimate_win_rate(self, nb_simulation, nb_player, hole_card, community_card=None):
        if not community_card: community_card = []

        # Make lists of Card objects out of the list of cards
        community_card = gen_cards(community_card)
        hole_card = gen_cards(hole_card)

        # Estimate the win count by doing a Monte Carlo simulation
        win_count = sum([self.montecarlo_sim(nb_player, hole_card, community_card) for _ in range(nb_simulation)])
        return 1.0 * win_count / nb_simulation

    # Do a Monte Carlo simulation given the current state of the game by evaluating the hands
    def montecarlo_sim(self, nb_player, hole_card, community_card):
        community_card = _fill_community_card(community_card, used_card=hole_card + community_card)
        unused_cards = _pick_unused_card((nb_player - 1) * 2, hole_card + community_card)
        opponents_hole = [unused_cards[2 * i:2 * i + 2] for i in range(nb_player - 1)]
        opponents_score = [HandEvaluator.eval_hand(hole, community_card) for hole in opponents_hole]
        my_score = HandEvaluator.eval_hand(hole_card, community_card)
        return 1 if my_score >= max(opponents_score) else 0

    #def bluff(self, play_suggestion, utilities):
    def bluff(self, score, hole, community):

        cards = hole + community
        raise_discount = .9
        all_in_discount = .2
        next_action = PokerConstants.Action.CALL

        if self.__is_straightflash(cards): score = score * 25
        if self.__is_fourcard(cards): score = score * 20
        if self.__is_fullhouse(cards): score = score * 14
        if self.__is_flash(cards): score = score * 10
        if self.__is_straight(cards): score = score * 8
        if self.__is_threecard(cards): score = score * 5
        if self.__is_twopair(cards): score = score * 3
        if self.__is_onepair(cards): score = score * 2

        for opp in self.opponent_state:
            if opp == PokerConstants.Action.FOLD:
                continue
            elif opp == PokerConstants.Action.CALL:
                continue
            elif opp == PokerConstants.Action.RAISE:
                score = score * raise_discount
            elif opp == PokerConstants.Action.ANTE:
                score = score * all_in_discount

        if score > 250:
            next_action = PokerConstants.Action.RAISE
        elif 250 > score > 100:
            next_action = PokerConstants.Action.CALL
        else:
            if len(community) > 4:
                next_action = PokerConstants.Action.CALL
            else:
                next_action = PokerConstants.Action.FOLD
        return next_action

    def declare_action(self, valid_actions, hole_card, round_state):
        # a valid action is a dictionary (tuple?) of the form {'action': 'fold', 'amount': 2}
        # needs both action name (fold, call, raise) and an amount

        # hole card is a length 2 list of the two cards (strings like 'DA', 'SK')

        # valid_actions format => [raise_action_info, call_action_info, fold_action_info]
        call_action_info = valid_actions[1]
        action, amount = call_action_info["action"], call_action_info["amount"]
        return action, amount   # action returned here is sent to the poker engine

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
        
