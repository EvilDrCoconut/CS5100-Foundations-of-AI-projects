# this class is from https://www.data-blogger.com/2017/11/01/pokerbot-create-your-poker-ai-bot-in-python/
#   and is being used for unit testing

from pypokerengine.players import BasePokerPlayer
import numpy as np
from sklearn.neural_network import MLPRegressor

# This is a basic class from PyPokerEngine used to make sure bots could play a game
class CallBot(BasePokerPlayer):
    def declare_action(self, valid_actions, hole_card, round_state):
        actions = [item for item in valid_actions if item['action'] in ['call']]
        return list(np.random.choice(actions).values())

    def receive_game_start_message(self, game_info):
        pass

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass


def setup_ai():
    return CallBot()