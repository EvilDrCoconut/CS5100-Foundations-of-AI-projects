# This class is used from https://www.data-blogger.com/2017/11/01/pokerbot-create-your-poker-ai-bot-in-python/
#   for unit testing

from pypokerengine.api.game import start_poker, setup_config
from testBot import testBot
from CallBot import CallBot
from pokerbot import PokerBot
import numpy as np
import csv

if __name__ == '__main__':

    pokerBotMinMax = PokerBot(1)
    pokerBotAlphaBeta = PokerBot(2)
    pokerBotExpecti = PokerBot(3)
    pokerBotBluff = PokerBot(4)


    pokerBot = PokerBot(1)

    testBot = testBot()


    stack_log = []
    pbminmax = []
    pbAlphaBeta = []
    pbExpecti = []
    pbBLuff = []

    pbMinMax_vs_pbBluff = []
    pbAlphaBeta_vs_pbBluff = []
    pbMinMax_vs_pbAlphaBeta = []
    

    for round in range(100):
        p1 = testBot ; p2 = pokerBotMinMax

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        pbminmax.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))
    print(pbminmax)
    print('\n', 'Next Test', '\n')

    stack_log = []
    for round in range(100):
        p1 = testBot ; p2 = pokerBotAlphaBeta

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        pbAlphaBeta.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))
    print(pbAlphaBeta)
    print('\n', 'Next Test', '\n')

    '''
    for round in range(100):
        p1 = testBot ; p2 = pokerBotExpecti

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBot.uuid])
        pbExpecti.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBot.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))
    print(pbExpecti)
    print('\n', 'Next Test', '\n')
    '''
    
    stack_log = []
    for round in range(100):
        p1 = testBot ; p2 = pokerBotBluff

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        pbBLuff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        print('Avg. stack:', '%d' % (int(np.mean(stack_log))))
    print(pbBLuff)
    print('\n', 'Next Test', '\n')

    stack_log = []
    stack_log2 = []
    for round in range(100):
        p1 = pokerBotMinMax ; p2 = pokerBotBluff

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        stack_log2.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        pbMinMax_vs_pbBluff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        pbMinMax_vs_pbBluff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        print('Avg. MinMax stack:', '%d' % (int(np.mean(stack_log))))
        print('Avg. Bluff stack:', '%d' % (int(np.mean(stack_log2))))
    print(pbMinMax_vs_pbBluff)
    print('\n', 'Next Test', '\n')

    stack_log = []
    stack_log2 = []
    for round in range(100):
        p1 = pokerBotAlphaBeta ; p2 = pokerBotBluff

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        stack_log2.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        pbAlphaBeta_vs_pbBluff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        pbAlphaBeta_vs_pbBluff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        print('Avg. AlphaBeta stack:', '%d' % (int(np.mean(stack_log))))
        print('Avg. Bluff stack:', '%d' % (int(np.mean(stack_log2))))
    print(pbAlphaBeta_vs_pbBluff)
    print('\n', 'Next Test', '\n')

    stack_log = []
    stack_log2 = []
    for round in range(100):
        p1 = pokerBotMinMax ; p2 = pokerBotAlphaBeta

        config = setup_config(max_round=5, initial_stack=1000, small_blind_amount=5)
        config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        game_result = start_poker(config, verbose=0)

        stack_log.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        stack_log2.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        pbMinMax_vs_pbAlphaBeta.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        pbMinMax_vs_pbAlphaBeta.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        print('Avg. MinMax stack:', '%d' % (int(np.mean(stack_log))))
        print('Avg. AlphaBeta stack:', '%d' % (int(np.mean(stack_log2))))
    print(pbMinMax_vs_pbAlphaBeta)
    print('\n', 'Done Testing, writing data to data.csv')

    with open('data3.csv', mode = 'w') as data_file:
        data_writer = csv.writer(data_file, delimiter='=', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(pbminmax); data_writer.writerow(pbAlphaBeta); data_writer.writerow(pbBLuff)
        data_writer.writerow(pbMinMax_vs_pbBluff); data_writer.writerow(pbAlphaBeta_vs_pbBluff); data_writer.writerow(pbMinMax_vs_pbAlphaBeta)