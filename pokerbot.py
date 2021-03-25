import random
from pypokerengine.players import BasePokerPlayer

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
    
    def bluff(self, play_suggestion, utilities):
        return

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
        
