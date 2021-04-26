
from pypokerengine.api.game import start_poker, setup_config
from testBot import testBot
from CallBot import CallBot
from pokerbot import PokerBot
import numpy as np
import csv
from agent import Agent


# This was a set up simulation for the Q-Learning bots vs the non learning bots
if __name__ == '__main__':
    pokerBotMinMax = PokerBot(1)
    pokerBotAlphaBeta = PokerBot(2)
    pokerBotBluff = PokerBot(4)

    teamVeyjaBot1 = Agent('p4')
    teamVeyjaBot2 = Agent('p5')
    teamVeyjaBot3 = Agent('p6')


    pbminmax = []
    pbAlphaBeta = []
    pbBLuff = []

    teamVeyjaBot1Data = []
    teamVeyjaBot2Data = []
    teamVeyjaBot3Data = []


    for round in range(500):
        p1 = pokerBotMinMax ; 
        p2 = pokerBotAlphaBeta; 
        p3 = pokerBotBluff
        p4 = teamVeyjaBot1; p5 = teamVeyjaBot2; p6 = teamVeyjaBot3

        config = setup_config(max_round=5, initial_stack=10000, small_blind_amount=10)
        #config.register_player(name="p1", algorithm=p1)
        config.register_player(name="p2", algorithm=p2)
        config.register_player(name="p3", algorithm=p3)
        config.register_player(name="p4", algorithm=p4)
        config.register_player(name="p5", algorithm=p5)
        config.register_player(name="p6", algorithm=p6)
        game_result = start_poker(config, verbose=0)

        #pbminmax.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotMinMax.uuid])
        pbAlphaBeta.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotAlphaBeta.uuid])
        pbBLuff.append([player['stack'] for player in game_result['players'] if player['uuid'] == pokerBotBluff.uuid])
        teamVeyjaBot1Data.append([player['stack'] for player in game_result['players'] if player['uuid'] == teamVeyjaBot1.uuid])
        teamVeyjaBot2Data.append([player['stack'] for player in game_result['players'] if player['uuid'] == teamVeyjaBot2.uuid])
        teamVeyjaBot3Data.append([player['stack'] for player in game_result['players'] if player['uuid'] == teamVeyjaBot3.uuid])
        print('Round Over')


with open('TeamLukeVsTeamVeyja.csv', mode = 'w') as data_file:
        data_writer = csv.writer(data_file, delimiter='=', quotechar = '"', quoting=csv.QUOTE_MINIMAL)
        data_writer.writerow(teamVeyjaBot1Data); data_writer.writerow(teamVeyjaBot2Data); data_writer.writerow(teamVeyjaBot3Data)
        #data_writer.writerow(pbminmax)
        data_writer.writerow(pbAlphaBeta)
        data_writer.writerow(pbBLuff)