

import random
from pypokerengine.engine.poker_constants import PokerConstants
import pypokerengine.engine.action_checker

def Poker_Bot(self):
    self.__initiate__()

    algorithm = random.randint(1, 4)
    current_algorithm = self.minimax()

    # needs to record opponents last movde
    opponents_last_move = []


    def bluff(score, hole, community):

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

        for opp in opponents_last_move:
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
