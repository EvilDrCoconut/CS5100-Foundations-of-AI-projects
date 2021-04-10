# This class is used from https://www.data-blogger.com/2017/11/01/pokerbot-create-your-poker-ai-bot-in-python/
#   for unit testing

from pypokerengine.api.game import start_poker, setup_config

from CallBot import CallBot
from pokerbot import PokerBot
import numpy as np

if __name__ == '__main__':
    #pokerBot = PokerBot()
    testBot = testBot()

    # The stack log contains the stacks of the Data Blogger bot after each game (the initial stack is 100)
    stack_log = []
    for round in range(100):
        p1 = testBot; p2 = CallBot() #; p3 = pokerBot

        config = setup_config(max_round=5, initial_stack=100, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == testBot.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))