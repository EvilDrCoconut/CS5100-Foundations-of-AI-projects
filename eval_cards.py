def eval_cards(cards):

    suits_by_card = {}
    ranks_by_card = {}
    vals = { 2: '2', 3: '3', 4: '4', 5 : '5',  6: '6',
             7: '7', 8: '8', 9: '9', 10: '10', 11: 'J',
             12: 'Q', 13: 'K', 14: 'A'}

    for card in cards:
        suit = card[:1]
        rank = card[1:]

        if suit in suits_by_card:
            suits_by_card[suit].append(rank)
        else:
            suits_by_card[suit] = [rank]

        if rank in ranks_by_card:
            ranks_by_card[rank].append(suit)
        else:
            ranks_by_card[rank] = [suit]

    straight = []
    vset = 0
    # Find straight flush
    for i in range(2, 14):
        for suit in suits_by_card.keys():
            if vals[i] in suits_by_card[suit]:
                vset += 1
            else:
                vset = 0
            if vset >= 5:
                return 25

    # Find four card
    for rank in ranks_by_card.keys():
        if len(ranks_by_card[rank]) == 4:
            return 22

    # Find full house
    hasThree = False
    hasPair = False'
    for rank in ranks_by_card.keys():
        if len(ranks_by_card[rank]) == 3:
            hasThree = True
        elif len(ranks_by_card[rank]) == 2:
            hasPair = True
        
        if hasPair and hasThree:
            return 19

    vset = 0
    # Find straight
    for i in range(2, 14):
        if vals[i] in ranks_by_card.keys():
            vset += 1
        else:
            vset = 0
        
        if vset >= 5:
            return 17

    # Find flush
    ranks = []
    for suit in suits_by_card.keys():
        if len(suits_by_card[suit]) >= 5:
            for card in suits_by_card[suit]:
                ranks.append(card[1:])
            return 15

    # Three of a kind
    for rank in ranks_by_card.keys():
        if len(ranks_by_card[rank]) == 3:
            return 12

    # Pairs
    pairs = 0
    for rank in ranks_by_card.keys():
        if len(ranks_by_card[rank]) == 2:
            pairs += 1
        if pairs == 2:
            return 8
        elif pairs == 1:
            return 4





    


    


